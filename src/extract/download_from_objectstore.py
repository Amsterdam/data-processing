###############################################################################
# functions to dowload data from the Cloud VPS Objectstore
###############################################################################

import os
import sys
sys.path.insert(0, '../')
import errno
import argparse
import datetime
import configparser
from swiftclient.client import Connection
from dateutil import parser as dateparser
from helper_functions import create_dir_if_not_exists
import logging

log = logging.getLogger(__name__)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('swiftclient').setLevel(logging.WARNING)


FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


def get_config(full_path):
    """Get config file with login credentials, port numbers..."""
    config = configparser.RawConfigParser()
    config.read(full_path)
    print("Found these configs:")
    for config_name in config.sections():
        print('-', config_name)
    return config


def get_connection(full_path, config_name):
    """
    get an objectsctore connection
    args:
        full_path:   path to the config.ini file where the config variables are stored
        config_name: the different configs as stated in the config file. Pick 'objectstore'
    returns
        swiftclient connection
    """
    config = configparser.RawConfigParser()
    config.read(full_path)
    

    OBJECTSTORE = dict(
        VERSION = config.get(config_name, 'VERSION'),
        AUTHURL = config.get(config_name, 'AUTHURL'),
        TENANT_NAME = config.get(config_name, 'TENANT_NAME'),
        TENANT_ID = config.get(config_name, 'TENANT_ID'),
        USER = config.get(config_name, 'USER'),
        #PASSWORD = os.environ['OBJECTSTORE_PASSWORD'],
        PASSWORD = config.get(config_name, 'PASSWORD'),
        REGION_NAME = config.get(config_name, 'REGION_NAME')
)
    
    connection = Connection(OBJECTSTORE)
    
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


def download_files(file_list, download_dir):
    """Download the latest data. """
    for source_data_file in file_list:
        sql_gz_name = source_data_file['name'].split('/')[-1]
        msg = 'Downloading: %s' % (sql_gz_name)
        
        create_dir_if_not_exists(download_dir)
        
        new_data = get_object(
            connection, source_data_file, 'Dataservices')
        
        print (type(download_dir), type(new_data))
        
        # save output to file!
        with open(download_dir + '{}'.format(sql_gz_name), 'wb') as outputzip:
            outputzip.write(new_data)


def get_full_container_list(conn, container, **kwargs) -> list:
    """
    get all files stored in container (incl. sub-containers)
    
    Args
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
    parser = argparse.ArgumentParser(description="""
Download data from the Objectstore, and write to local directory
To test run this command line: 
""")
    parser.add_argument('config_file',
                        help='weukfwkefy')
    parser.add_argument('connection', 
                        help="""a connection to the Objectstore""")
    parser.add_argument('meta_data', 
                        help='the meatadate of the files in the specified containers')
    
    return parser


def main():
    args = parser().parse_args()
    config = get_config(arg.config_file)
    connection = get_connection(args.full_path, args.config)
    #get_expected_files(....TO DO)
    

if __name__ == "__main__":
    main()