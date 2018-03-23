#!/usr/bin/env python

import argparse
from datapunt_processing import logger

# If you need generic helper functions, put them in our helpers folder
# or reuse the current ones by using this import:
# from helpers.files import create_dir_if_not_exists, unzip, save_file


# Setup logging service
logger = logger()


def your_second_function(argname1, argname2):
    """
    Does some great stuff.

    Args:
        1. argname1: path/in/store
        2. argname2: your_file_name.txt

    Returns:
        A file or check, show some examples.
    """

    data = argname1
    something = data
    logger.info('Another Succes!')
    return something


def your_first_function(argname1):
    """
    Does some great stuff.

    Args:
        argname1: path/in/store

    Returns:
        A file or check, show some examples.
    """
    something_2 = 'test2'
    logger.info('Succes!')
    return something_2


def parser():
    """
    Parser function to run arguments from commandline and to add description to sphinx docs.
    To see possible styling options: https://pythonhosted.org/an_example_pypi_project/sphinx.html
    """
    description = """
    Explain what this function does, and add a full commandline example which works:

    Use ENV:
        ``export NAME=envvalue``

    Example command line:
        ``python this_cool_function.py first_argument second_argument``
    """

    parser = argparse.ArgumentParser(
                        description=description)
    parser.add_argument('first_arg',
                        type=str,
                        help='Explain what must go in, with example.')
    parser.add_argument('second_arg',
                        type=str,
                        help='Specify the desired output folder path, for example: app/data')
    return parser


def main():
    # Return all arguments in a list
    args = parser().parse_args()

    # Run all functions sequential
    your_first_function(args.first_arg, args.second_arg)
    your_second_function(args.second_arg)


if __name__ == "__main__":
    main()
