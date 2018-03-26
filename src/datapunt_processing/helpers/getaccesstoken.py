# utf-8
import requests
import os
import random
import string
import argparse
from urllib.parse import urlparse, parse_qsl
from datapunt_processing import logger

log = logger()


class GetAccessToken(object):
    """
        Get an header authentication item for access token
        for using the internal API's by logging in as with email and password credentials and authenticated scopes or as type 'employee'
        To see the available scopes and types, see this file:
            https://github.com/Amsterdam/authorization_levels/blob/master/authorization_levels.py
        Usage:
            from authentication.getaccesstoken import GetAccessToken

            accessToken = GetAccessToken().getAccessToken(usertype='employee_plus', scopes=BRK/RS,BRK/RSN,BRK/RO)
            requests.get(url, headers=accessToken)

        Args:
            - scopes: Add scopes as a comma separated list.
            - usertype: Add the usertype
            - email: Set and get environment variable: export DATAPUNT_EMAIL=*****
            - password: Set and get environment variable: export DATAPUNT_PASSWORD=*****
        Returns:
            accesstoken
    """

    def getAccessToken(self, usertype='employee', scopes='TLLS/R', acc=False):
        def randomword(length):
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(length))

        authzUrl = 'https://api.data.amsterdam.nl/oauth2/authorize'

        # check_url = urlparse(redirect_uri).netloc.split('.')[0]
        redirect_uri = 'https://data.amsterdam.nl/'

        if acc is True:
            authzUrl = 'https://acc.api.data.amsterdam.nl/oauth2/authorize'
            redirect_uri = 'https://acc.data.amsterdam.nl/'

        scopes = scopes.replace(',',' ')

        params = {
            'idp_id': 'datapunt',
            'response_type': 'token',
            'client_id': 'citydata',
            'scope': scopes,
            'state': randomword(10),
            'redirect_uri': redirect_uri
        }

        def scrub(item_tuple):
            """Hide the token credentials in the console."""
            item_tuple=list(item_tuple)
            if item_tuple[0].strip().endswith('token'):
                item_tuple[1] = '<hidden token>'
            if item_tuple[0].strip().endswith('credentials'):
                item_tuple[1] = '<hidden credentials>'
            return item_tuple

        def printUrlParameterMessage(url):
            parsed = urlparse(location)
            query = parse_qsl(parsed.query)
            for item in query:
                item = scrub(item)
                log.info('Message: {} {}'.format(item[0], item[1]))

        response = requests.get(authzUrl, params, allow_redirects=False)

        if response.status_code == 303:
            location = response.headers["Location"]
            printUrlParameterMessage(location)
        else:
            log.info('Error in parameters.')
            return {}

        if usertype == 'employee_plus':
            assert os.environ.get('DATAPUNT_EMAIL')
            assert os.environ.get('DATAPUNT_PASSWORD')
            data = {
                'type': 'employee_plus',
                'email': os.environ.get("DATAPUNT_EMAIL"),
                'password': os.environ.get('DATAPUNT_PASSWORD')
            }
        if usertype == 'employee':
            # Use authentication of default user
            data = {
               'type': 'employee'
            }

        response = requests.post(location, data=data, allow_redirects=False)
        if response.status_code == 303:
            location = response.headers["Location"]
            printUrlParameterMessage(location)
        else:
            log.info('Error retrieving token')
            return {}

        response = requests.get(location, allow_redirects=False)
        if response.status_code == 303:
            returnedUrl = response.headers["Location"]
            printUrlParameterMessage(returnedUrl)
        else:
            log.info('Error retrieving token')
            return {}

        # Get grantToken from parameter aselect_credentials in session URL
        parsed = urlparse(returnedUrl)
        fragment = parse_qsl(parsed.fragment)
        for item in fragment:
            item = scrub(item)
            log.info('Message: {} {}'.format(item[0], item[1]))

        access_token = fragment[0][1]
        if access_token != {}:
            os.environ["ACCESS_TOKEN"] = access_token
            log.info(f'Received new Access Token Header') #{access_token}')
            return {"Authorization": 'Bearer ' + access_token}
        else:
            log.info('Error retrieving token')


def parser():
    """
    Parser function to run arguments from commandline and to add description to sphinx docs.
    To see possible styling options: https://pythonhosted.org/an_example_pypi_project/sphinx.html
    """
    description = """
    Explain what this function does, and add a full commandline example which works:

    Example command line:
        ``python getaccesstoken.py employee_plus BRK/RO https://acc.api.data.amsterdam.nl``
        ``python getaccesstoken.py employee TLLS/R https://acc.api.data.amsterdam.nl``
    """

    parser = argparse.ArgumentParser(
                        description=description)
    parser.add_argument('usertype',
                        type=str,
                        choices=['employee', 'employee_plus'],
                        default='employee',
                        help='Choose user type')
    parser.add_argument('scopes',
                        type=str,
                        help='Choose scopes, the names can be found here: https://github.com/Amsterdam/authorization_levels/blob/master/authorization_levels.py. For example: TLLS/R or multiple: BRK/RS,BRK/RSN,BRK/RO')
    parser.add_argument('-a', action='store_true',
                        help="Use option -a to use acc uri's, default False to use production uri's.")

    return parser


if __name__ == "__main__":
    args = parser().parse_args()
    access_token = GetAccessToken().getAccessToken(usertype=args.usertype,
                                                   scopes=args.scopes,
                                                   acc=args.a
                                                   )
    os.environ["ACCESS_TOKEN"] = access_token
