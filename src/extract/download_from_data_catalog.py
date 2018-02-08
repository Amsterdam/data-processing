#!/usr/bin/env python
"""
Download the latest shapefiles.
"""
import os
import shutil
import argparse
import pprint
import requests
import zipfile


def unzip(path, filename_as_folder=False):
    """Find all .zip files and unzip in root, use filename_as_folder=True to unzip to subfolders with name of zipfile."""
    for filename in os.listdir(path):
        if filename.endswith(".zip"):
            name = os.path.splitext(os.path.basename(filename))[0]
            if not os.path.isdir(name):
                try:
                    file = os.path.join(path, filename)
                    zip = zipfile.ZipFile(file)
                    if filename_as_folder:
                        directory = os.path.join(path, name)
                        os.mkdir(directory)
                        print("Unzipping {} to {}".format(filename, directory))
                        zip.extractall(directory)
                    else:
                        print("Unzipping {} to {}".format(filename, path))
                        zip.extractall(path)
                except zipfile.BadZipfile:
                    print("BAD ZIP: " + filename)
                    try:
                        os.remove(file)
                    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
                        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
                            raise  # re-raise exception if a different error occured                


def download(metadata_id, download_directory):
    """Download files from data catalog response id"""
    METADATA_URL = 'https://api.data.amsterdam.nl/catalogus/api/3/action/package_show?id={}&dtfs=T&mpb=topografie&mpz=11&mpv=52.3731081:4.8932945'.format(metadata_id)
    print("Downloading metadata from", METADATA_URL)
    metadata_res = requests.get(METADATA_URL)
    metadata_res.raise_for_status()

    metadata = metadata_res.json()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(metadata)

    for result in metadata['result']['resources']:
        if result['url_type'] is not None or result['url_type'] == 'upload':
            filename = result['url'].split('/')[-1]
            print('Downloading ' + filename)
            download_file(result['url'], os.path.join(download_directory,filename))


def download_file(file_location, target):
    print("Downloading File from", file_location)
    file = requests.get(file_location, stream=True)
    file.raise_for_status()
    with open(target, 'wb') as f:
        file.raw.decode_content = True
        shutil.copyfileobj(file.raw, f)
    print("Downloaded as", target)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get data from data catalog')
    parser.add_argument('metadata_id', help='Insert Metadata id from data catalog, for example: 5d84c216-b826-4406-8297-292678dee13c')
    parser.add_argument('data_path', help='Insert folder path, for example: app/data')
    args = parser.parse_args()
    download(args.metadata_id, args.data_path)
    unzip(args.data_path)
