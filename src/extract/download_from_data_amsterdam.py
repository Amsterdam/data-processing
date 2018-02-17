#!/usr/bin/env python

import sys
sys.path.insert(0, '../transform/helper_functions/')
import os, errno
import shutil
import argparse
import pprint
import requests
import urllib.parse as urlparse
from helper_functions import create_dir_if_not_exists, unzip



def get_catalog_package_id(url):
    """
    Retrieve package id from full url from data.amsterdam.nl, for example: catalogus/api/3/action/package_show?id=c1f04a62-8b69-4775-ad83-ce2647a076ef
    """
    decoded_url = urlparse.unquote(url)
    parsed_url = urlparse.urlparse(decoded_url)
    meta_id = urlparse.parse_qs(parsed_url.fragment)['?dte'][0]
    return meta_id


def download_metadata(url):
    """
    Download files from data catalog response id
    """
    package_id = get_catalog_package_id(url)
    METADATA_URL = 'https://api.data.amsterdam.nl/{}&dtfs=T&mpb=topografie&mpz=11&mpv=52.3731081:4.8932945'.format(package_id)
    print("Downloading metadata from", METADATA_URL)
    metadata_res = requests.get(METADATA_URL)
    metadata_res.raise_for_status()

    metadata = metadata_res.json()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(metadata)
    return metadata


def download_all_files(metadata, download_directory):
    """
    Download all files from metadata resources list
    """
    for result in metadata['result']['resources']:
        if result['url_type'] is not None or result['url_type'] == 'upload':
            filename = result['url'].split('/')[-1]
            print('Downloading ' + filename)

            create_dir_if_not_exists(download_directory)

            download_file(result['url'], os.path.join(download_directory, filename))


def download_file(file_location, target):
    print("Downloading File from", file_location)
    file = requests.get(file_location, stream=True)
    file.raise_for_status()

    with open(target, 'wb') as f:
        file.raw.decode_content = True
        shutil.copyfileobj(file.raw, f)
    print("Downloaded as", target)


def parser():
    """Parser function to run arguments from commandline and to add description to sphinx."""
    parser = argparse.ArgumentParser(description="""
Get data and metadata from data.amsterdam.nl, unzip if needed and put the file in a local directory.
To test run this command line::

download_from_data_amsterdam https://data.amsterdam.nl/#?dte=catalogus%2Fapi%2F3%2Faction%2Fpackage_show%3Fid%3D5d84c216-b826-4406-8297-292678dee13c app/data
""")
    parser.add_argument('url', help="""
Insert full url from main result page of dataset, 
for example: https://data.amsterdam.nl/#?dte=catalogus%2Fapi%2F3%2Faction%2Fpackage_show%3Fid%3D5d84c216-b826-4406-8297-292678dee13c&dtfs=T&mpb=topografie&mpz=11&mpv=52.3731081:4.8932945
""")
    parser.add_argument('output_folder', help='Specify the desired output folder path, for example: app/data')
    #parser.add_argument('--f','filename_as_folder', default=False, help='use --f=True to unzip to subfolders with name of zipfile.')
    return parser


def main():
    args = parser().parse_args()
    metadata = download_metadata(args.url)
    download_all_files(metadata, args.output_folder)
    unzip(args.output_folder)


if __name__ == "__main__":
    main()
