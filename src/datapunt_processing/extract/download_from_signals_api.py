import requests
import pandas as pd
import numpy as np
import os
import random
import string
from urllib.parse import urlparse, parse_qsl
from datapunt_processing import logger
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# config
pd.set_option('display.max_columns', 100)
logger = logger()


class GetAccessToken(object):
    """
    Get a header authentication item for access token for using
    the internal API's by logging in as type = 'employee'
    Usage:
     from accesstoken import AccessToken
     getToken = AccessToken()
     accessToken = getToken.getAccessToken()
     requests.get(url, headers= accessToken)
    """
    def getAccessToken(self, email, password, acceptance):

        def randomword(length):
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(length))

        state = randomword(10)
        scopes = ['SIG/ALL']
        acc_prefix = 'acc.' if acceptance else ''
        authUrl = f'https://{acc_prefix}api.data.amsterdam.nl/oauth2/authorize'
        params = {
            'idp_id': 'datapunt',
            'response_type': 'token',
            'client_id': 'citydata',
            'scope': ' '.join(scopes),
            'state': state,
            'redirect_uri': f'https://{acc_prefix}data.amsterdam.nl/'
        }
        print('url', authUrl)
        response = requests.get(authUrl, params, allow_redirects=False)
        if response.status_code == 303:
            location = response.headers["Location"]
        else:
            return {}

        data = {
            'type': 'employee_plus',
            'email': email,
            'password': password,
        }

        response = requests.post(location, data=data, allow_redirects=False)
        if response.status_code == 303:
            location = response.headers["Location"]
        else:
            return {}

        response = requests.get(location, allow_redirects=False)
        if response.status_code == 303:
            returnedUrl = response.headers["Location"]
        else:
            return {}

        # Get grantToken from parameter aselect_credentials in session URL
        parsed = urlparse(returnedUrl)
        fragment = parse_qsl(parsed.fragment)
        access_token = fragment[0][1]
        os.environ["ACCESS_TOKEN"] = access_token
        return access_token

# acceptance = False
# email = os.getenv('SIGNALS_USER', '')
# password = os.getenv('SIGNALS_PASSWORD', '')
# bearer_token = GetAccessToken().getAccessToken(email, password, acceptance)


URL = "https://api.data.amsterdam.nl/signals/auth/signal/?&page_size=1000"

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


def get_sia_json(url, params, bearer_token):
    """
    first: put SIGNALS_USER en SIGNALS_PASSWORD to env variables (!)
    Args:
        url: sia api endpoint
        params: created_at, main_cat, sub_cat, text, address, pc,
                bc, sd, geometry, status or provide lists/dicts of values
        bearer_token: bearer_token
    Returns:
        parsed json or error message
    """
    session = _get_session_with_retries()
    next_page = url
    # start looping thorugh pages,store in result_list
    result_list = []

    # while next_page is not None:
    while next_page:
        logger.debug('Grabbing %s', next_page)
        response = session.get(next_page, params=params,
                               headers={"Authorization": "Bearer " + bearer_token})
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

            result_list.append(result_dict)
        # break (if you want only one page)

    return result_list
