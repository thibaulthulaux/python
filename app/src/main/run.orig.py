#!/usr/bin/env python3
"""
Module Docstring
"""

""" ----------------------------------------------------------------------- """
__author__ = "Thibault HULAUX"
__version__ = "0.1.0"
__license__ = "MIT"

""" ----------------------------------------------------------------------- """
from argparse import ArgumentParser
import logging # see https://docs.python.org/3/library/logging.html
import logging.config
import os
import sys
# import docker

""" ----------------------------------------------------------------------- """
def readLines(path):
    return open(path, "r").read().splitlines()

def getRealPath(path):
    return os.path.realpath(path)


""" ----------------------------------------------------------------------- """
def loggerAll(logger):
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')


def init():
    global logger
    logging.config.fileConfig(fname='conf/logging.conf', disable_existing_loggers=False)
    logger = logging.getLogger(os.path.basename(__file__))
    logger.debug(args)


""" ----------------------------------------------------------------------- """
def main(args):
    """ Main entry point of the app """
    init()

    # client = docker.from_env()
    # client = docker.DockerClient(base_url='tcp://127.0.0.1')

    # client.containers.run('alpine', 'echo hello world')


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("arg", help="Required positional argument")

    # Optional argument flag which defaults to False
    parser.add_argument("-f", "--flag", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-n", "--name", action="store", dest="name")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()

    main(args)




    
    sys.exit(0)
