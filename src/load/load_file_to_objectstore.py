#!/usr/bin/env python
import os
import argparse
import logging
from mimetypes import MimeTypes
import urllib

from helpers.connections import objectstore_connection
from helpers.files import create_dir_if_not_exists

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger(__name__)


def put_object(
        connection, container: str, filename: str,
        contents, content_type: str) -> None:
    """
    Upload file to objectstore
    Args
    :container == "path/in/store"
    :object_name = "your_file_name.txt"
    :contents=thefiledata (fileobject) open('ourfile', 'rb')
    :content_type='text/csv'  / 'application/json' .. using the mime package
    """
    logger.info('Uploading file...')
    connection.put_object(
        container, filename, contents=contents,
        content_type=content_type)


def get_object(connection, container_path, filename, output_folder):
    """
    Download file from objectstore container.

    Args
    : connection = Objectstore connection based on from helpers.connection import objectstore_connection
    : container_path = Name of container/prefix/subfolder
    : filename = Name of file, for example test.csv
    : output_folder = Define the path to write the file to for example app/data when using docker.
    """
    resp_headers, obj_contents = connection.get_object(container, filename)
    with open(os.path.join(output_folder, filename), 'w') as local:
        local.write(obj_contents)


def check_existence_object(connection, container_path, filename):
    """
    Check if the file is present on the objectstore container_path,
    Args
    : connection = Objectstore connection based on from helpers.connection import objectstore_connection
    : container_path = Name of container/prefix/subfolder
    : filename = Name of file, for example test.csv
    Result
    'The object was not found'
    """
    try:
        resp_headers = connection.head_object(container_path, filename)
        logger.info('The object was successfully created')
    except ClientException as e:
        if e.http_status == '404':
            logger.info('The object was not found')
        else:
            logger.info('An error occurred checking for the existence of the object')


def upload_file(connection, container_path, filename_path):
    """
    Upload file to the objectstore
    Args
    : connection = Objectstore connection based on from helpers.connection import objectstore_connection
    : container_path = Name of container/prefix/subfolder, for example Dataservices/aanvalsplan_schoon/crow
    : filename_path = full path including the name of file, for example: data/test.csv

    Uses mime for content_type: https://stackoverflow.com/questions/43580/how-to-find-the-mime-type-of-a-file-in-python
    """
    with open(filename_path, 'rb') as contents:
        mime = MimeTypes()
        content_type = mime.guess_type(filename_path)[0]
        logging.info("Found content type '{}'".format(content_type))
        filename = os.path.basename(filename_path)
        put_object(connection, container_path, filename, contents, content_type)
        check_existence_object(connection, container_path, filename)


def parser():
    """Parser function to run arguments from commandline and to add description to sphinx docs."""
    description = """
    Write a file to a container on the objectstore.
    Use: export OBJECTSTORE_PASSWORD=********** to your environment before running this command script.
    `load_file_to_objectstore config.ini objectstore data/test.csv Dataservices/aanvalsplan_schoon/crow`
    """

    parser = argparse.ArgumentParser(
                        description=description)
    parser.add_argument('config_path',
                        type=str,
                        help='Define the full path of the config file, for example /path_to_config/config.ini or config.ini')
    parser.add_argument('config_name',
                        type=str,
                        help='Specify the name in the config.ini file, for example objectstore')
    parser.add_argument('filename',
                        type=str,
                        help='Specify the name of the file')
    parser.add_argument('container_path',
                        type=str,
                        help='Specify the full container and prefix path where to upload to, Dataservices/aanvalsplan_schoon/crow')
    return parser


def main():
    # Return all arguments in a list
    args = parser().parse_args()
    connection = objectstore_connection(args.config_path, args.config_name)
    upload_file(connection, args.container_path, args.filename)


if __name__ == "__main__":
    main()
