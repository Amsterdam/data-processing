#!/usr/bin/env python
import os
import argparse
import logging
from datapunt_processing.helpers.connections import objectstore_connection
from datapunt_processing.helpers.files import create_dir_if_not_exists

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger(__name__)


def get_full_container_list(connection, container, **kwargs):
    """
    Get all files stored in container (incl. sub-containers)

    Args:
        1. connection: connection session using the objectstore_connection function from the helpers.connections
        2. container: "name of the root container/folder in objectstore"

    Returns:
        Generator object with all containers.
    """
    # Note: taken from the bag_services project
    limit = 10000
    kwargs['limit'] = limit
    page = []

    seed = []

    _, page = connection.get_container(container, **kwargs)
    seed.extend(page)

    while len(page) == limit:
        # keep getting pages..
        kwargs['marker'] = seed[-1]['name']
        _, page = connection.get_container(container, **kwargs)
        seed.extend(page)

    return seed


def download_container(connection, container, prefix, output_folder):
    """
    Download file from objectstore.

    Args:
        1. connection: connection session using the objectstore_connection function from the helpers.connections
        2. prefix: tag or folder name of file, for example subfolder/subsubfolder
        3. output_folder = '/{folder}/ '

    Returns:
        Written file /{folder}/{prefix}/{file}
    """
    target_dir = os.path.join(output_folder, prefix)
    create_dir_if_not_exists(target_dir)
    content = get_full_container_list(connection, container['name'], prefix=prefix)
    # print(content)
    for obj in content:
        if obj['content_type'] != 'application/directory':
            target_filename = os.path.join(output_folder, obj['name'])
            with open(target_filename, 'wb') as new_file:
                _, obj_content = connection.get_object(container['name'], obj['name'])
                new_file.write(obj_content)
            logger.info('Written file {}'.format(target_filename))


def download_containers(config_path, config_name, prefixes, output_folder):
    """
    Download multiple files from the objectstore.

    Args:
        1. connection: connection session using the objectstore_connection function from the helpers.connections
        2. prefixes: multiple folders where the files are located, for example aanvalsplan_schoon/crow,aanvalsplan_schoon/mora
        3. output_folder: local folder to write files into, for example app/data for a docker setup

    Result:
        Loops through download_container function for each prefix (=folder)
    """
    logger.debug('Setting up objectstore connection')
    connection = objectstore_connection(config_path, config_name)

    logger.debug('Checking local data directory exists and is empty')
    if not os.path.exists(output_folder):
        raise Exception('Local data directory does not exist.')

    # logger.debug('Establishing object store connection.')
    resp_headers, containers = connection.get_account()

    logger.info('Downloading containers ...')
    prefixes = prefixes.split(',')
    print(containers)
    print(prefixes)
    for container in containers:
        for prefix in prefixes:
            download_container(connection, container, prefix, output_folder)


def parser():
    """Parser function to run arguments from commandline and to add description to sphinx docs."""
    description = """
    Download files from the objectstore:
    ``download_from_objectstore config.ini objectstore aanvalsplan_schoon/crow,aanvalsplan_schoon/mora data``

    Use ``export OBJECTSTORE_PASSWORD=**********`` to add the password to your environment before running this command script.
    """

    parser = argparse.ArgumentParser(
                        description=description)
    parser.add_argument('config_path',
                        type=str,
                        help='Define the full path of the config file, for example /path_to_config/config.ini or config.ini')
    parser.add_argument('config_name',
                        type=str,
                        help='Specify the name in the config.ini file, for example objectstore')
    parser.add_argument('prefixes',
                        type=str,
                        help='Specify the names of the folders to download, separated by a comma, for example aanvalsplan_schoon/crow, aanvalsplan_schoon/mora')
    parser.add_argument('output_folder',
                        type=str,
                        help='Specify the output_folder location, for example data')
    return parser


def main():
    # Return all arguments in a list
    args = parser().parse_args()
    download_containers(args.config_path, args.config_name, args.prefixes, args.output_folder)


if __name__ == "__main__":
    main()
