#!/usr/bin/env python

import argparse
import requests
import requests_cache
from datapunt_processing.helpers.getaccesstoken import GetAccessToken
from datapunt_processing.helpers.files import save_file
from datapunt_processing import logger

# Setup logging service
logger = logger()


def getJsonData(url, accessToken):
    """
    Get a json response from a url with accesstoken.

    Args:
        1. url: api endpoint
        2. accessToken: acces token generated using the auth helper:
           GetAccessToken().getAccessToken(usertype='employee_plus',
                                           scopes='BRK/RS,BRK/RSN/,BRK/RO')

    Returns:
        parsed json or error message
    """  # noqa
    response = requests.get(url, headers=accessToken)  # Get first page for count
    if response.status_code != 200:
        if response.status_code == 404 or response.status_code == 401:
            logger.info('Error status: {} {}'.format(str(response.status_code),
                                                     "trying with trailing / ..."))
            response = requests.get(url + '/', headers=accessToken)
        else:
            return logger.info('Error status: ' + str(response.status_code))
    jsonData = response.json()
    logger.info("recieved data from {} ".format(url))
    return jsonData


def parser():
    """Parser function to run arguments from commandline and to add description to sphinx docs."""  # noqa
    parser = argparse.ArgumentParser(description="""
    Download from the BRK API from api.data.amsterdam.nl using the
    OAuth2 datapunt Authorization service with employee_plus credentials.

    Use ENV::

        export DATAPUNT_EMAIL=***
        export DATAPUNT_PASSWORD=***

    Command line example::

        download_from_api_brk https://api.data.amsterdam.nl/brk/object/ BRK/RS,BRK/RSN,BRK/RO data object.json

    """)
    parser.add_argument(
        'url',
        type=str,
        help='add full endpoint, for example:\
              https://api.data.amsterdam.nl/brk/object/')
    parser.add_argument(
        'scopes',
        type=str,
        help='Choose scopes, the names can be found here:\
              https://github.com/Amsterdam/authorization_levels/blob/master/authorization_levels.py.\
              For example: TLLS/R or multiple: BRK/RS,BRK/RSN,BRK/RO')
    parser.add_argument(
        'output_folder',
        type=str,
        help='add outputfolder location, for example:\
              my_project_folder/data')
    parser.add_argument(
        'filename',
        type=str,
        help='add filename for example brk.json')
    return parser


def main():
    # Return all arguments in a list
    args = parser().parse_args()
    logger.info("Getting Access token.")
    accessToken = GetAccessToken().getAccessToken(usertype='employee_plus', scopes=args.scopes)
    logger.info("Setup temp database to store requests to speed up restart download if network fails.")
    requests_cache.install_cache('requests_db', backend='sqlite')

    json_data = getJsonData(args.url, accessToken)
    logger.info(json_data)
    save_file(json_data, args.output_folder, args.filename)


if __name__ == "__main__":
    main()
