import argparse
import requests
import json
from helpers.logging import logger

logger = logger()

BASE_URL = "https://api.kvk.nl/api/v2/search/companies?"
error_key = ''

def get_kvk_json(url, params, api_key = None):
    """
    Get a json response from a url, provided params + api_key.
    Args:
        url: api endpoint
        params: kvkNumber, branchNumber, rsin, street, houseNumber, postalCode, 
                city, tradeName, or provide lists/dicts of values
        api_key: kvk api_key
    Returns:
        parsed json or error message
    """
    response = requests.get(url, params) 
    
    if api_key:
        url += '&user_key={}'.format(API_KEY)
    else:
        return logger.error('please provide api_key')
    
    try:
        response.raise_for_status() # Raises stored :class:`HTTPError`, if one occurred
    except requests.exceptions.HTTPError as e:
        raise errors.InvalidResponse(response) from e
    json_response = response_to_json(response)
    return json_response


def response_to_json(response):
    try:
        json_response = response.json()['data']
    except json.decoder.JSONDecodeError as e:
        raise errors.DecodeError() from e
    if isinstance(json_resp, dict):
        if bool(json_resp.get(error_key, False)):
            raise logger.error('Error status: {}'.format(errors.InvalidResponse(response)))
    logger.info("received data from {} ".format(url))
    return json_response


def parser():
    """Parser function to run arguments from commandline and to add description to sphinx docs."""
    description = """
    call the kvk api for the nationwide ' handelsregister':
    ``EXAMPLE: ...........``
    Use ``export API_KEY=**********`` to add the API_KEY to your environment before running this command script.
    """

    parser = argparse.ArgumentParser(
                        description=description)
    parser.add_argument('url',
                        type=str,
                        help='Define the full API path')
    parser.add_argument('params',
                        type=dict,
                        help='Specify the parameters for our api call in a dict')
    parser.add_argument('api_key',
                        type=str,
                        help='Specify api_key that you added to your ENVIRONMENT variables')

    return parser

def main():
    # Return all arguments in a list
    args = parser().parse_args()
    json_data = get_kvk_json(args.url, args.params, args.api_key)
    
if __name__ == "__main__":
    main()