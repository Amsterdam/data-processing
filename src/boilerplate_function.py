#!/usr/bin/env python

import argparse

# If you need helper_functions, put them in our helper_function library or re-use them:
# From helper_functions import create_dir_if_not_exists, unzip


def your_second_function(argname1):
    data = argname1
    something = 'test'
    return something


def your_first_function(argname2):
    something_2 = 'test2'
    return something_2


def parser():
    """Parser function to run arguments from commandline and to add description to sphinx docs."""
    description = """
Explain what this function does, and add a full commandline example which works:
python this_cool_function.py this_is_some_argument this_is_the_second_argument
                  """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('first_arg', type=str, help="""Explain what must go in, with example.""")
    parser.add_argument('second_arg',type=str, help='Specify the desired output folder path, for example: app/data')
    return parser


def main():
    # Return all arguments in a list
    args = parser().parse_args()
    # Run all functions sequential
    your_first_function(args.first_arg)
    your_second_function(args.second_arg)


if __name__ == "__main__":
    main()
