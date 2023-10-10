#!/usr/bin/env python3
"""
extract_mohc.py

Extract CMORised files from the MASS tape archive and store them in a DRS 
directory structure.
"""
import argparse
from pathlib import Path, PurePosixPath
from subprocess import check_output, CalledProcessError, STDOUT
from xml.etree import ElementTree

import yaml


def run_command(command):
    """
    Run the command specified and return any output to stdout or stderr as
    a list of strings.

    :param str command: The complete command to run.
    :returns: Any output from the command as a list of strings.
    :raises RuntimeError: If the command did not complete successfully.
    """
    cmd_out = None
    try:
        cmd_out = check_output(command, stderr=STDOUT, shell=True).decode("utf-8")
    except CalledProcessError as exc:
        msg = (
            "Command did not complete sucessfully.\ncommand:\n{}\n"
            "produced error:\n{}".format(command, exc.output)
        )
        raise RuntimeError(msg)

    if isinstance(cmd_out, str):
        return cmd_out.rstrip().split("\n")
    else:
        return None


def cdds_to_drs_path(uri):
    """
    Take a relative path in the CDDS directory structure and convert this to
    a DRS directory structure, i.e. remove the 'embargoed' directory.

    >>> cdds_to_drs_path(PurePosixPath("mip_era", "activity_id", "institution_id", "source_id", "experiment_id", "member_id", "table_id", "variable_id", "grid_label", "embargoed", "version", "filename.nc"))
    PurePosixPath('mip_era/activity_id/institution_id/source_id/experiment_id/member_id/table_id/variable_id/grid_label/version/filename.nc')

    :param pathlib.PurePosixPath uri: The CDDS relative path
    :returns: The equivalent DRS path
    :rtype: pathlib.PurePosixPath
    """
    return PurePosixPath("").joinpath(*uri.parts[:9], *uri.parts[-2:])


def parse_args():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser(description="Extract CMORised files")
    parser.add_argument(
        "yaml_file",
        action="store",
        help="The YAML configuration file to control extraction",
    )
    args = parser.parse_args()

    return args


def main(args):
    """
    Main entry point
    """
    with open(args.yaml_file) as yaml_handle:
        config = yaml.safe_load(yaml_handle)

    with open(config["xml_file"]) as xml_handle:
        tree = ElementTree.parse(xml_handle)

    for node in tree.iter():
        if node.tag == "nodes":
            continue
        uri = PurePosixPath(node.attrib.get("url"))
        if uri.match("*.nc"):
            # This is a file rather than directory
            print(uri)
            mass_root = PurePosixPath(config["OUTPUT_MASS_ROOT"]).joinpath(
                PurePosixPath(config["OUTPUT_MASS_SUFFIX"])
            )
            drs = uri.relative_to(mass_root)
            drs_corrected = cdds_to_drs_path(drs)
            dest_path = Path(config["gws_root"]).joinpath(drs_corrected)
            dest_dir = dest_path.parent
            if not dest_dir.exists():
                dest_dir.mkdir(parents=True)
            print(dest_path)
            run_command(f"moo get {uri} {dest_path}")
            print()


if __name__ == "__main__":
    cmd_args = parse_args()
    main(cmd_args)
