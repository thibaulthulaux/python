#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Thibault HULAUX"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse

import logging # see https://realpython.com/python-logging/

# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.basicConfig(
  level=logging.DEBUG,
  filename='python.log',
  filemode='w',
  format='%(asctime)s - %(message)s',
  datefmt='%d-%b-%y %H:%M:%S')

name = 'John'
logging.error(f'{name} raised an error.')

a = 5
b = 0

try:
  c = a / b
except Exception as e:
  logging.error('Exception occured', exc_info=True)

try:
  c = a / b
except Exception as e:
  logging.exception('Exception occured')

# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')



def main(args):
    """ Main entry point of the app """

    logging.debug(args)


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
