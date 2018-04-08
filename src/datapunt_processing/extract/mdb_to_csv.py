#!/usr/bin/env python

import argparse
import subprocess
import os

from datapunt_processing import logger
from datapunt_processing.helpers.files import create_dir_if_not_exists

# Setup logging service
logger = logger()


def get_tables_mdb(mdb_file):
    """Get the list of table names with "mdb-tables" for a *.mdb file using latin1 as encoding.
    """
    table_names_binary_string = subprocess.Popen(["mdb-tables", "-1", mdb_file],
                                                 stdout=subprocess.PIPE).communicate()[0]
    table_names = table_names_binary_string.decode('latin1')  # other option could be 'ascii'
    tables = table_names.split('\n')
    logger.info("Available tables:{}".format(tables))
    return tables


def dump_mdb_tables_to_csv(mdb_file, output_folder, table_names):
    """Dump each table as a CSV file using "mdb-export"
       and converting " " in table names to "_" for the CSV filenames."""
    create_dir_if_not_exists(output_folder)
    if table_names is None:
        tables = get_tables_mdb(mdb_file)
    else:
        tables = table_names[0].split(',')

    for table in tables:
        if table != '':
            filename = os.path.join(output_folder, table.replace(" ", "_") + ".csv")
            file = open(filename, 'wb')
            logger.info("Dumping " + table)
            contents = subprocess.Popen(["mdb-export", mdb_file, table],
                                        stdout=subprocess.PIPE).communicate()[0]
            file.write(contents)
            file.close()


def parser():
    """
    Parser function to run arguments from commandline and to add description to sphinx docs.
    To see possible styling options: https://pythonhosted.org/an_example_pypi_project/sphinx.html
    """
    parser = argparse.ArgumentParser(description="""
    A simple script to dump the tables of a Microsoft Access Database to multiple CSV files.

    It depends upon the mdbtools suite.

    To install the suite:
    Linux: `sudo apt install mdbtools`
    OSX:  `brew install mdbtools`
    Windows:  https://github.com/lsgunth/mdbtools-win but not tested, check this thread: https://github.com/brianb/mdbtools/issues/107

    If not using the --tables_names it dumps all tables.

    Example command line to dump all tables:
        ``python mdb_to_csv.py test.mdb data``

    Example command line to dump specific tables:
        ``python mdb_to_csv.py test.mdb data --table_names VM_GEGEVENS,VM_RVVCODE``
    """)
    parser.add_argument(
        'mdb_file',
        type=str,
        help='filename and location of mdb file, for example data/test.mdb')
    parser.add_argument(
        'output_folder',
        type=str,
        help='Specify the desired output folder path, for example: app/data')
    parser.add_argument(
        '--table_names',
        type=str,
        nargs='+',
        default=None,
        help='Optional argument. Standard all tables are dumped,\
              You can use this option to specify one or more table names,\
              For example:--table_names VM_GEGEVENS,VM_RVVCODE')
    return parser


def main():
    # Return all arguments in a list
    args = parser().parse_args()
    dump_mdb_tables_to_csv(args.mdb_file, args.output_folder, args.table_names)


if __name__ == "__main__":
    main()
