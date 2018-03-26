#!/usr/bin/env python

import argparse
import requests
import requests_cache
from datapunt_processing.helpers.getaccesstoken import GetAccessToken
from datapunt_processing.helpers.files import save_file
from datapunt_processing import logger

# If you need generic helper functions, put them in our helpers folder
# or reuse the current ones by using this import:
# from helpers.files import create_dir_if_not_exists, unzip, save_file


# Setup logging service
logger = logger()


def retrywithtrailingslash(url, access_token):
    response = requests.get(url, headers=access_token)  # Get first page for count
    if response.status_code != 200:
        if response.status_code == 404 or response.status_code == 401:
            logger.info('Error status: {} {}'.format(str(response.status_code), "trying with trailing / ..."))
            response = requests.get(url + '/', headers=access_token)
            return response
        else:
            return logger.info('Error status: ' + str(response.status_code))
    return response


def getJsonData(url, access_token):
    """
    Get a json response from a url with accesstoken.

    Args:
        1. url: api endpoint
        2. accessToken: acces token generated using the auth helper: GetAccessToken().getAccessToken(usertype='employee_plus', scopes='BRK/RS,BRK/RSN/,BRK/RO')

    Returns:
        parsed json or error message
    """

    response = retrywithtrailingslash(url, access_token)

    json_data = response.json()
    logger.info("recieved data from {} ".format(url))
    return json_data


def parser():
    """Parser function to run arguments from commandline and to add description to sphinx docs."""
    description = """
    Generic download function to download data from authenticated endpoints on api.data.amsterdam.nl using the authentication/getaccesstoken.py script:

    You can login as 2 types of users:

    - employee::

        For endpoints which are only viewable when on the internal network.

      uses::

        data={type='employee'}

    - employee_plus credentials.

      For endpoints which require a user/password which can be given, by filling in this form::

         http://intranet.amsterdam.nl/kennis-beleid/dienstverlening/data/programma-datapunt/autorisatie-datapunt/ 

      and sending it to::

          datapunt@amsterdam.nl

      uses::

          data={type='employee', email='<registered email>', password='<recieved password'}

    When using the employee_plus type add the following ENV variables::

        export DATAPUNT_EMAIL=***
        export DATAPUNT_PASSWORD=***

    Command line example using employee for tellus api's on acc::

        download_from_api_brk https://acc.api.data.amsterdam.nl/tellus/tellusdata employee TLLS/R data tellus.json

    Command line example using employee_plus for kadaster api's on acc::

        download_from_api_brk https://acc.api.data.amsterdam.nl/brk/object/ employee_plus BRK/RS,BRK/RSN,BRK/RO data object.json
    """

    parser = argparse.ArgumentParser(
                        description=description)
    parser.add_argument('url',
                        type=str,
                        help='add full endpoint, for example https://api.data.amsterdam.nl/brk/object/')
    parser.add_argument('usertype',
                        type=str,
                        choices=['employee', 'employee_plus'],
                        default='employee',
                        help='Choose user type employee or employee_plus')
    parser.add_argument('scopes',
                        type=str,
                        help='Define scopes of the endpoints, the names can be found here: https://github.com/Amsterdam/authorization_levels/blob/master/authorization_levels.py. For example: TLLS/R or multiple: BRK/RS,BRK/RSN,BRK/RO')
    parser.add_argument('output_folder',
                        type=str,
                        help='Add outputfolder location, for example: my_project_folder/data or . if you want to save in the current dir')
    parser.add_argument('filename',
                        type=str,
                        help='Add filename: for example brk.json')
    return parser


def main():
    # Return all arguments in a list
    args = parser().parse_args()

    logger.info("Getting Access token.")
    access_token = GetAccessToken().getAccessToken(usertype=args.usertype, scopes=args.scopes)

    logger.info("Setup temp database to store requests to speed up restart download if network fails.")
    requests_cache.install_cache('requests_db', backend='sqlite')

    logger.info("Getting data with Access token.")
    json_data = getJsonData(args.url, access_token)
    logger.info(json_data)

    save_file(json_data, args.output_folder, args.filename)


if __name__ == "__main__":
    main()
