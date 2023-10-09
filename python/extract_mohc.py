#!/usr/bin/env /apps/jasmin/jaspy/miniconda_envs/jaspy3.10/m3-4.9.2/envs/jaspy3.10-m3-4.9.2-r20220721/bin/python
"""
extract_mohc.py

Extract CMORised files from the MASS tape archive and store them in a DRS 
directory structure.
"""
import argparse
from subprocess import check_output, CalledProcessError, STDOUT
from xml.etree import ElementTree


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
        cmd_out = check_output(command, stderr=STDOUT,
                               shell=True).decode('utf-8')
    except CalledProcessError as exc:
        msg = ("Command did not complete sucessfully.\ncommand:\n{}\n"
               "produced error:\n{}".format(command, exc.output))
        raise RuntimeError(msg)

    if isinstance(cmd_out, str):
        return cmd_out.rstrip().split("\n")
    else:
        return None


def to_drs(uri):
    """
    Take the MASS URI specfied and return the DRS path. This removes the     
    additional directory level that was added by the CDDS.

    :param str uri: The MASS URI where the file currently is.
    :returns: The DRS path of the file.
    :rtype: str
    """



def parse_args():
    """
    Parse command-line arguments
    """
    parser = argparse.ArgumentParser(description="Extract CMORised files")
    parser.add_argument("XML_file", action="store",
                        help="The XML file listing to restore")
    args = parser.parse_args()

    return args


def main(args):
    """
    Main entry point
    """
    with open(args.XML_file) as f:
        tree = ElementTree.parse(f)

    for node in tree.iter():
        if node.tag == "nodes":
            continue
        uri = node.attrib.get("url")
        if uri.endswith(".nc"):
            print(url)


if __name__ == "__main__":
    cmd_args = parse_args()
    main(cmd_args)
