import requests
import argparse
import pandas as pd
import numpy as np
import os
import random
import string
from urllib.parse import urlparse, parse_qsl

from datapunt_processing import logger
from datapunt_processing.helpers.getaccesstoken import GetAccessToken
from datapunt_processing.helpers.files import create_dir_if_not_exists, save_file

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


# config
pd.set_option('display.max_columns', 100)
logger = logger()


# zie https://www.peterbe.com/plog/best-practice-with-retries-with-requests

EMPTY = np.nan


def _get_session_with_retries():
    """
    Get a requests Session that will retry some set number of times.
    """
    session = requests.Session()

    retries = Retry(
        total=5,
        backoff_factor=0.1,
        status_forcelist=[500, 502, 503, 504],
        raise_on_status=True
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('https://', adapter)
    session.mount('http://', adapter)

    return session


def process_address(location):
    """Extract """
    fields = ('openbare_ruimte', 'postcode', 'woonplaats', 'huisnummer')
    out = {}
    if location['address'] and isinstance(location['address'], dict):
        for field in fields:
            out[field] = location['address'].get(field, EMPTY)
    else:
        out = {field: EMPTY for field in fields}

    return out


def get_sia_json(url, scope, params, acc=False, page_limit=0):
    """
    first: put SIGNALS_USER en SIGNALS_PASSWORD to env variables (!)

    Args:
        url: sia api endpoint
        params: created_at, main_cat, sub_cat, text, address, pc, bc, sd, geometry, status or provide lists/dicts of values
        bearer_token: bearer_token

    Returns:
        parsed json or error message
    """
    access_token = GetAccessToken().getAccessToken(usertype='employee_plus', scopes=scope, acc=acc)
    # print(access_token)
    session = _get_session_with_retries()
    next_page = url
    # start looping through pages,store in result_list
    result_list = []
    page = 0
    while next_page and int(page) != int(page_limit) + 1 :
        logger.debug('Grabbing %s', next_page)
        response = session.get(next_page, params=params, headers=access_token)
        result = response.json()

        next_page = result['_links']['next']['href']
        logger.debug('Next page %s', next_page)
        for i, item in enumerate(result['results']):
            result_dict = {}

            # indicate what to extract
            result_dict['created_at'] = item['created_at']
            result_dict['main_cat'] = item['category']['main']
            result_dict['sub_cat'] = item['category']['sub']
            result_dict['text'] = item['text']
            result_dict.update(process_address(item['location']))
            result_dict['bc'] = item['location'].get('buurt_code', EMPTY)
            result_dict['sd'] = item['location'].get('stadsdeel', EMPTY)
            result_dict['geometry'] = item['location']['geometrie']['coordinates']
            result_dict['status'] = item['status']['state']
            # print(result_dict)
            result_list.append(result_dict)
        # break (if you want only one page)
        page += 1
        logger.info("{} signals retrieved".format(page*1000))

    return result_list


def parser():
    """
    Parser function to run arguments from commandline and to add description to sphinx docs.
    To see possible styling options: https://pythonhosted.org/an_example_pypi_project/sphinx.html
    """
    description = """
    Download all signals from https://api.data.amsterdam.nl/signals

    Use ENV for login credentials to use the API:
        ``export DATAPUNT_EMAIL=xxxx``
        ``export DATAPUNT_PASSWORD=xxxxx``

    Example command line:
        ``python download_from_signals_api.py https://api.data.amsterdam.nl/signals/auth/signal/?&page_size=1000 SIG/ALL created_at,main_cat,sub_cat,text,address,pc,bc,sd,geometry 1 data sia.json``
    """

    parser = argparse.ArgumentParser(
                        description=description)
    parser.add_argument('url',
                        type=str,
                        help='Url of endpoint, for example: https://api.data.amsterdam.nl/signals/auth/signal')
    parser.add_argument('scope',
                        type=str,
                        help='Specify which scope you have access to as list with no spaces, for example: SIG/ALL,TLLS/R')
    parser.add_argument('params',
                        type=str,
                        help='Add which fields to extract as a list: created_at,main_cat,sub_cat,text,address,pc,bc,sd,geometry')
    parser.add_argument('page_limit',
                        type=int,
                        help='number of pages to get, standard 1000 records per page, default all')
    parser.add_argument('output_folder',
                        type=str,
                        help='Output folder, for example: data')
    parser.add_argument('filename',
                        type=str,
                        help='name the file with .json')

    return parser


def main():
    args = parser().parse_args()
    data = get_sia_json(args.url, args.scope, args.params, args.page_limit)
    save_file(data, args.output_folder, args.filename)

if __name__ == "__main__":
    main()
