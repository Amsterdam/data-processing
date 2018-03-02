###############################################################################
# functions to dowload data from the Cloud VPS Objectstore
###############################################################################

import os
import sys
import errno
import argparse
import datetime
import configparser
from swiftclient.client import Connection
from dateutil import parser as dateparser
from helpers.files import create_dir_if_not_exists

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger('objectstore')


def get_config(full_path):
    """
    Get config file with login credentials, port numbers...
    Args:
        full_path - provide path tot he config file/ auth.conf etc.
    """
    config = configparser.RawConfigParser()
    config.read(full_path)
    logger.info('Found these configs.. {}'.format(config.sections()))
    return config


def get_connection(full_config_path, config_name, print_config_vars=None):
    """
    get an objectsctore connection
    args:
        full_path:   path to the config.ini file where the config variables are stored
        config_name: the different configs as stated in the config file. Pick 'objectstore'
        print_config_vars: if set to True: print all variables from the config file
    returns
        swiftclient connection
    """
    config = get_config(full_config_path)

    OBJECTSTORE = dict(
        VERSION=config.get(config_name, 'VERSION'),
        AUTHURL=config.get(config_name, 'AUTHURL'),
        TENANT_NAME=config.get(config_name, 'TENANT_NAME'),
        TENANT_ID=config.get(config_name, 'TENANT_ID'),
        USER=config.get(config_name, 'USER'),
        # PASSWORD=os.environ['OBJECTSTORE_PASSWORD'],
        PASSWORD=config.get(config_name, 'PASSWORD'),
        REGION_NAME=config.get(config_name, 'REGION_NAME')
    )
    logger.info('Connecting to config..: {}'.format(config_name))

    if print_config_vars:
        logger.info('config variables.. :{}'.format(OBJECTSTORE))

    connection = Connection(OBJECTSTORE)
    logger.info('Established successfull connection.. {}'.format(OBJECTSTORE['AUTHURL']))

    return connection


def get_object(connection, object_meta_data: dict, dirname: str):
    """
    extract file from objectstore
    Args:
        connection = swiftclient connection to Objectstore
        object_meta_data = dictionary of files with metadata on OS
        dirname = '/../ '
    returns:
    """
    return connection.get_object(dirname, object_meta_data['name'])[1]


def get_full_container_list(conn, container, **kwargs) -> list:
    """
    get all files stored in container (incl. sub-containers)
    Args:
        conn = connection with the Objectstore (using swiftclient Connection API)
        container == "path/in/Objectstore"
    returns
        generator object
    """
    limit = 10000
    kwargs['limit'] = limit
    page = []

    _, page = conn.get_container(container, **kwargs)
    lastpage = page

    for object_info in lastpage:
        yield object_info

    while len(lastpage) == limit:
        # keep getting pages..
        kwargs['marker'] = lastpage['name']
        _, lastpage = conn.get_container(container, **kwargs)
        for object_info in lastpage:
            yield object_info

    raise StopIteration


def get_expected_files(EXPECTED_FILES:list):
    """
    Download the expected files provided by EXPECTED_FILES list
    for instance: get_expected_files(EXPECTED_FILES=['aanvalsplan_schoon/mora/MORA_data_2014_2017_sel.csv']) 
    """
    file_list = []

    for obj in meta_data:
        for expected_file in EXPECTED_FILES:
            if not obj['name'].endswith(expected_file):
                continue

            dt = dateparser.parse(obj['last_modified'])
            now = datetime.datetime.now()

            delta = now - dt

            log.debug('AGE: %d %s', delta.days, expected_file)

            log.debug('%s %s', EXPECTED_FILES, dt)
            file_list.append((obj))
            print (dt, file_list)

    download_files(file_list, 'app/data/')


def parser():
    """Parser function to run arguments from commandline and to add description to sphinx."""
    desc = """
        Download data from the Objectstore, and write the files to a local directory
        To test run this command line:
        download_from_objectstore config.ini objectstore data
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('full_config_path',
                        help='The location of the configuration file path including the name: for example config.ini when it is the same folder.')
    parser.add_argument('objecstore_config',
                        help="""Connection settings name of the objectstore url, user/pasword and project/tennant id. Stored in config.ini""")
    parser.add_argument('output_folder',
                        help="""Outputfolder location, for example my_project_folder/data or . if you want to save in the current dir.""")
    #parser.add_argument('meta_data',
    #                    help='the meatadate of the files in the specified containers')
    return parser


def main():
    args = parser().parse_args()
    connection = get_connection(args.full_config_path, args.objecstore_config)
    
    # get_expected_files(....TO DO)


if __name__ == "__main__":
    main()
