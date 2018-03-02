# utf-8
import requests
import os
import random
import string
from urllib.parse import urlparse, parse_qsl

class GetAccessToken(object):
    """
        Get an header authentication item for access token
        for using the internal API's
        by logging in as type = 'employee'

        Usage:
            from accesstoken import AccessToken
            getToken = AccessToken()
            accessToken = getToken.getAccessToken()
            requests.get(url, headers= accessToken)
    """
    def getAccessToken(self):

        def randomword(length):
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(length))

        state = randomword(10)
        scopes = ['TLLS/R']
        authzUrl = 'https://api.data.amsterdam.nl/oauth2/authorize'
        params = {
            'idp_id' : 'datapunt',
            'response_type' : 'token',
            'client_id' : 'citydata',
            'scope' : ' '.join(scopes),
            'state' : state,
            'redirect_uri' : 'https://data.amsterdam.nl/'
        }

        response = requests.get(authzUrl, params, allow_redirects=False)
        if response.status_code == 303:
            location = response.headers["Location"]
        else:
            return {}

        data = {
            'type':'employee'
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
        print(f'Received new Access Token Header') #{access_token}')
        return {"Authorization": 'Bearer ' + access_token}


if __name__ == "__main__":
    access_token = GetAccessToken().getAccessToken()
    print(f'Received new Access Token Header: {access_token}')
