#!/usr/bin/env python3
"""
Module Docstring
"""

""" IMPORTS ----------------------------------------------------------------------- """
import argparse
import logging # see https://docs.python.org/3/library/logging.html
import logging.config
import os
import platform
import sys
import time

""" GLOBALS ----------------------------------------------------------------------- """
# Default LOGLEVEL
os.environ['LOGLEVEL'] = 'DEBUG'

# System
__env__ = os.environ
__start__ = time.time()
__platform__ = platform.system()

# Authoring
__authorname__ = 'Thibault HULAUX'
__authormail__ = 'thibault.hulaux@gmail.com'
__version__ = '0.0.0'
__license__ = 'MIT'

# Magic file and folder paths
__basename__ = os.path.basename(__file__)
__basenamenoext__ = __basename__.split(".", 1)[0]
__dirname__ = os.path.dirname(__file__)

# Help strings
__description__ = f'{__basename__} short description.'
__epilog__ = f'Run {__basename__} [command] --help for more information on a command.'


def init_logger(
        config = 'conf/logging.conf',
        filename = f'{__basenamenoext__}.log',
        filepath = ''
        ):
    """"""
    logger = None
    
    # Add filename and filepath to logging
    logging.filename = filename
    logging.filepath = filepath

    # Load config file
    logging.config.fileConfig(
        fname = config,
        disable_existing_loggers=False
    )
    
    # Set log level from env
    # logging.config f'{__env__["LOGLEVEL"]}'

    # Create logger
    logger = logging.getLogger(__basename__)
    return logger

def init_parser():
    parser = None

    # Create parser
    parser = argparse.ArgumentParser(
        add_help = True,
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description=__description__,
        epilog=__epilog__
    )

    # Add debug argument
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        default=False
    )
    
    # Add version argument
    parser.add_argument(
        '--version',
        action='version',
        version=f'{__basename__} (version {__version__}) {__authorname__} - {__authormail__}'
    )
    
    return parser

""" MAIN -------------------------------------------------------------------------- """
def main():
    # Change working directory to script location
    os.chdir(__dirname__)
    
    # Init logger
    logger = init_logger()

    # Init parser
    parser = init_parser()
    parser.add_argument()
    # Parse args
    args = parser.parse_args()
    logger.debug(f'args={args}')
    
    # args = parser.parse_args()
    # logger.debug(f'args={args}, args.subcommand={args.subcommand}')
    # if args.subcommand is None:
    #     parser.print_help()
    # else:
    #     args.func(args)

    # Debug:
    # print("User's Environment variable:")
    # pprint.pprint(dict(__env__), width = 1)

    # Execution time
    logger.debug(f'Execution time: {(time.time()-__start__)*10**3:.03f} ms')

""" RUNTIME ----------------------------------------------------------------------- """
if __name__ == '__main__':
    """ This is executed when run from the command line """
    main()
sys.exit(0)