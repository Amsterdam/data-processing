#!/usr/bin/env python

import argparse
import requests
from helpers.logging import logger

# Setup logging service
logger = logger()


def upload_file_to_ckan(url, dataset_name, file_path):
    """
    Upload a file to the CKAN datastore.

    Args:
        1. url: url of the catalog::

            https://api.data.amsterdam.nl/catalogus

        2. dataset_name: name of the dataset, which can be found on the ckan page url::

            https://api.data.amsterdam.nl/catalogus/dataset/afvalcontainers

        3. api_key: your private user key, which can be found on the user profile page.
        4. file_path: location of the file including filename::

            /path/to/file/to/upload.csv

    Returns:
        An uploaded file to the CKAN datastore.
    """
    assert CKAN_API_KEY

    requests.post(url+'/api/action/resource_create',
              data={"package_id": dataset_name},
              headers={"X-CKAN-API-Key": api_key},
              files=[('upload', file(file_path))])
    logger.info('Uploaded {} to https://api.data.amsterdam.nl/catalogus/dataset/{}'.format(file_path.split('/')[-1], data_set_name))


def parser():
    """
    Parser function to run arguments from commandline and to add description to sphinx docs.
    To see possible styling options: https://pythonhosted.org/an_example_pypi_project/sphinx.html
    """
    description = """
    Upload a file to the CKAN datastore with your private user key, which can be found on the user profile page.

    Use ENV :
        ``export CKAN_API_KEY=********-****-****-****-************``

    Example command line:
        ``python load_file_to_ckan.py https://api.data.amsterdam.nl/catalogus afvalcontainers **apikey** ``
    """

    parser = argparse.ArgumentParser(
                        description=description)
    parser.add_argument('url',
                        type=str,
                        help="""url of the catalog::

                                    https://api.data.amsterdam.nl/catalogus
                             """)
    parser.add_argument('dataset_name',
                        type=str,
                        help="""name of the dataset, which can be found on the ckan page url::

                                    https://api.data.amsterdam.nl/catalogus/dataset/afvalcontainers
                             """)
    parser.add_argument('file_path',
                        type=str,
                        help="""location of the file including filename::

                                    /path/to/file/to/upload.csv
                             """)
    return parser


def main():
    # Return all arguments in a list
    args = parser().parse_args()

    # Run all functions sequential
    upload_file_to_ckan(args.url, args.dataset_name, args.file_path)



if __name__ == "__main__":
    main()
