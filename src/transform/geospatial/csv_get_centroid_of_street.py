
import requests
import requests_cache
import csv
import sys
import argparse


def get_centroid_street(filename, street_column, city_name):
    """
    Get the X,Y centroid of an address.

    Args:
        1. street_column: Dam 1
        2. city_name: Amsterdam
    Returns:
        Origional CSV file with coordinates and BAG corrected naming.
    """
    # fileName = 'test'
    csv_name = filename + '_coord.csv'
    with open(filename, 'r') as inputFile:
        header = False
        reader = csv.DictReader(inputFile, dialect='excel')
        with open(csv_name, 'w') as output_file:
            for row in reader:
                for fieldName in reader.fieldnames:
                    if fieldName.lower() in ('straatnaam','adres','straat', 'openbareruimtenaam'):
                       continue
                    elif len(sys.argv) == 2:
                        print('Please give the name of the street column...')
                        filename = input('Enter column Name: ')
                    else:
                        street_column = sys.argv[2]
                    try:
                        getUrl = "http://geodata.nationaalgeoregister.nl/locatieserver/free?q={}&woonplaatsnaam={}&fl=centroide_ll,straatnaam,score".format(row[street_column],city_name)
                        result = requests.get(getUrl)
                        resultJson = result.json()
                        print(getUrl)
                        # print(resultJson['response'])
                        if result.status_code == 200 and resultJson['response']['numFound'] != 0:
                            for item in resultJson['response']['docs']:
                               if item['score'] == resultJson['response']['maxScore']:
                                    del item['score']
                                    row.update(item)
                        else:
                            print('No results found')
                    except result.status_code as statusError:
                        print(statusError)

                    w = csv.DictWriter(output_file, row.keys())
                    if header == False:
                        w.writeheader()
                        header = True
                    w.writerow(row)

def parser():
    description = """
    Get the centroid of streetnames in a city using::

        https://github.com/PDOK/locatieserver/wiki/API-Locatieserver

    Command line example::

        python get_centroid_street_NED.py ../../tests/transform/testdata/centroid_street.csv straatnaam amsterdam

    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('file', help='Add filename location: example/test.csv')
    parser.add_argument('street_column', help='Header name of the address column')
    parser.add_argument('city', help='Add the name of the city, for example: Amsterdam')
    return parser


def main():
    args = parser().parse_args()
    # save api requests to temporary sqlite db for use with many reoccuring names
    requests_cache.install_cache('requests_cache', backend='sqlite')  # , expire_after=180)
    get_centroid_street(args.file, args.street_column, args.city)


if __name__ == "__main__":
    main()
