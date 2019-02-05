import requests
import json
import os
import errno
import csv
import time
import argparse
import logging
from datapunt_processing.helpers.getaccesstoken import GetAccessToken


def logger():
    """
    Setup basic logging for console.

    Usage:
        Initialize the logger by adding the code at the top of your script:
        ``logger = logger()``

    TODO: add log file export
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')
    logger = logging.getLogger(__name__)
    return logger


# Setup logging service
logger = logger()

# ------------------
#: File System stuff
# ------------------


def create_dir_if_not_exists(directory):
    """
    Create directory if it does not yet exists.

    Args:
        Specify the name of directory, for example: `dir/anotherdir`

    Returns:
        Creates the directory if it does not exists, of return the error message.
    """
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def save_file(data, output_folder, filename):
    """
        save_file currently works with: csv, txt, geojson and json as suffixes.
        It reads the filename suffix and saves the file as the appropriate type.

        Args:
            1. data: list of flattened dictionary objects for example: [{id:1, attr:value, attr2:value}, {id:2, attr:value, attr2:value}]
            2. filename: data_output.csv or data_output.json
            3. output_folder: dir/anotherdir

        Returns:
            Saved the list of objects to the given geojson or csv type.
    """
    create_dir_if_not_exists(output_folder)
    suffix = filename.split('.')[-1]
    full_path = os.path.join(output_folder, filename)
    if suffix in ('geojson', 'json'):
        with open(full_path, 'w') as out_file:
            json.dump(data, out_file, indent=2)
    if suffix in ('csv', 'txt'):
        with open(full_path, 'w') as out_file:
            # get header titles based on first object in array
            header = list(data[0].keys())
            csvWriter = csv.writer(out_file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            csvWriter.writerow(header)
            for row in data:
                csvWriter.writerow(row.values())
        with open(full_path, 'r') as rows:
            print('# --------------------------------------------------- ')
            print('# Copy rows below and paste in document. Save as .csv ')
            print('# --------------------------------------------------- ')
            print(rows.read())


# ----------------------
#: Main script functions
# ----------------------


def getPage(url, access_token=None):
    """
    Get data from url.
    Evaluate if employee credentials are present in environment variables.
    export DATAPUNT_EMAIL=*******
    export DATAPUNT_PASSWORD=******

    If present, get an accesstoken.
    Args:
        url
    Returns:
        response data
    """
    if access_token:
        data = requests.get(url, headers=access_token)
        # pprint('Show json results')
        # pprint(data.json(), indent=4)
    else:
        data = requests.get(url)

    return data.json()


def getDatasets(url, dcatd_url):
    """
    Parse each dataset json response into a non-nested dict structure.
    """
    data = []
    print(os.environ)
    if "DATAPUNT_EMAIL" in os.environ:
        access_token = GetAccessToken().getAccessToken(usertype='employee_plus', scopes='CAT/W')
        catalog_data = getPage(url, access_token)
        # pprint('Show json results')
        # pprint(data.json(), indent=4)
    else:
        catalog_data = getPage(url)

    for i, dataset in enumerate(catalog_data['dcat:dataset']):
        dataset_url = '{}/{}'.format(url, dataset['dct:identifier'])
        dataset_data = getPage(dataset_url)
        # pprint(dataset_data, indent=4)
        dataset_meta = {}
        dataset_meta['status'] = dataset['ams:status']
        dataset_meta['dataset'] = dataset_data['dct:title']
        dataset_meta['eigenaar'] = dataset_data['ams:owner']
        dataset_meta['licentie'] = dataset_data['ams:license']
        dataset_meta['thema'] = dataset_data['dcat:theme'][0].split(':')[1]
        dataset_meta['dataset publicatiedatum'] = dataset_data['foaf:isPrimaryTopicOf']['dct:issued']
        dataset_meta['dataset wijzigingsdatum'] = dataset_data['foaf:isPrimaryTopicOf']['dct:modified']
        dataset_meta['dataset frequentie'] = dataset_data['dct:accrualPeriodicity']
        dataset_meta['dataset url'] = '{}{}'.format(dcatd_url, dataset_data['dct:identifier'])
        dataset_meta['inhoudelijk contactpersoon'] = dataset_data['dcat:contactPoint']['vcard:fn']
        dataset_meta['inhoudelijk email'] = dataset_data['dcat:contactPoint']['vcard:hasEmail']
        dataset_meta['technisch contactpersoon'] = dataset_data['dct:publisher']['foaf:name']
        dataset_meta['technisch email'] = dataset_data.get('dct:publisher',{}).get('foaf:mbox', '')
        for resource in dataset_data['dcat:distribution']:
            row = {}
            row['resource'] = resource['dct:title']
            row['resource type'] = resource['ams:resourceType']
            row['resource wijziging'] = resource.get('dct:modified', '')
            row['resource purl'] = resource['ams:purl']
            row.update(dataset_meta)
            data.append(row)
            # print('{}, {} added'.format(dataset_data['dct:title'], resource['dct:title']))
        print('{} of {} added'.format(i, len(catalog_data['dcat:dataset'])))
    return data


def parser():
    """
    Parser function to run arguments from commandline and to add description to sphinx docs.
    To see possible styling options: https://pythonhosted.org/an_example_pypi_project/sphinx.html
    """
    description = """
    Script to generate a complete CSV table and writes it to a folder containing all resources available on https://data.amsterdam.nl
    This script uses the dcatd API. Swagger documentation can be found here:

    https://api.data.amsterdam.nl/api/swagger/?url=/dcatd/openapi

    Example command line:
        ``python download_all_resources_from_dcatd_to_csv.py output catalog``

    To get a list of disabled datasets, you need an upload account and set these to the environment variables:

    - export DATAPUNT_EMAIL=*******
    - export DATAPUNT_PASSWORD=******
    """

    parser = argparse.ArgumentParser(
                        description=description)
    parser.add_argument('output_folder',
                        type=str,
                        help='Specify the desired output folder path, for example: app/data')
    parser.add_argument('filename',
                        type=str,
                        help='Filename without .csv suffix, for example: catalog')
    return parser


def main():
    args = parser().parse_args()
    url = 'https://api.data.amsterdam.nl/dcatd/datasets'
    dcatd_url = 'https://data.amsterdam.nl/#?dte=dcatd/datasets/'

    data = getDatasets(url, dcatd_url)

    date = time.strftime("%d-%m-%Y")
    full_filename = '{}-{}.csv'.format(args.filename, date)

    save_file(data, args.output_folder, full_filename)


if __name__ == '__main__':
    main()
