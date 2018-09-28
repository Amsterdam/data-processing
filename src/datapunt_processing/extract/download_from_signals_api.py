import requests
import pandas as pd
pd.set_option('display.max_columns', 100)
from datetime import timedelta
import requests
import os
import random
import string
from urllib.parse import urlparse, parse_qsl
from random import randint
import time
import datetime
from datapunt_processing import logger
import copy

logger = logger()

class GetAccessToken(object):
    """
        Get a header authentication item for access token
        for using the internal API's
        by logging in as type = 'employee'
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
        authzUrl = f'https://{acc_prefix}api.data.amsterdam.nl/oauth2/authorize'
        params = {
            'idp_id': 'datapunt',
            'response_type': 'token',
            'client_id': 'citydata',
            'scope': ' '.join(scopes),
            'state': state,
            'redirect_uri' : f'https://{acc_prefix}data.amsterdam.nl/'
        }
        print('url', authzUrl)
        response = requests.get(authzUrl, params, allow_redirects=False)
        if response.status_code == 303:
            location = response.headers["Location"]
        else:
            return {}

        data = {
            'type':'employee_plus',
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


url = "https://api.data.amsterdam.nl/signals/auth/signal/?&page_size=1000"


def fill_empty_value(x):
    # Converts None to empty string
    ret = copy.deepcopy(x)
    # Handle dictionaries, lits & tuples. Scrub all values
    if isinstance(x, dict):
        for k, v in ret.items():
            ret[k] = scrub(v)
    if isinstance(x, (list, tuple)):
        for k, v in enumerate(ret):
            ret[k] = scrub(v)
    if x is None:
        ret = 'empty'
    return ret

        
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
    
    response= requests.get(url, params, headers = {"Authorization":"Bearer " + bearer_token})
    
    try:
        response.raise_for_status() # Raises 'HTTPError', if one occurred
    except requests.exceptions.HTTPError as e:
        raise errors.InvalidResponse(response) from e
        
    result = response.json()
    next_page = result['_links']['next']['href']
    logger.info("received data from {} ".format(url))
        
    
    # start looping though pages, store in result_list
    result_list = []

    while 'http' in str(next_page):

        r = requests.get(next_page, params, headers = {"Authorization":"Bearer " + bearer_token})
        result = r.json()

        next_page = result['_links']['next']['href']
        for item in result['results']:
            
            item = fill_empty_value(item)

            result_dict = {}

            # indicate what to extract   
            result_dict['created_at'] = item['created_at']
            result_dict['main_cat'] = item['category']['main']
            result_dict['sub_cat'] = item['category']['sub']
            result_dict['text'] = item['text']
            result_dict['address'] = item['location']['address_text']
            #result_dict['address'] = item['location']['address']['openbare_ruimte']
            result_dict['bc'] = item['location']['buurt_code']
            result_dict['sd'] = item['location']['stadsdeel']
            result_dict['geometry'] = item['location']['geometrie']['coordinates']
            result_dict['status'] = item['status']['state']

            result_list.append(result_dict)

            print(len(result_list))

    return result_list