
import requests
import requests_cache
import csv
import sys
import argparse



def get_centroid_street(street_column, city_name):
    # fileName = 'test'
    csvName = fileName + '_coord.csv'
    with open(fileName, 'r') as inputFile:
        header = False
        reader = csv.DictReader(inputFile, dialect='excel')
        with open(csvName, 'w') as outputFile:
            for row in reader:
                for fieldName in reader.fieldnames:
                    if fieldName.lower() in ('straatnaam','adres','straat', 'openbareruimtenaam'):
                       continue
                    elif len(sys.argv) == 2:
                        print('Please give the name of the street column...')
                        fileName = input('Enter column Name: ')
                    else:
                        fieldName = sys.argv[2]
                    try:
                        getUrl = "http://geodata.nationaalgeoregister.nl/locatieserver/free?q=%s AND woonplaatsnaam:Amsterdam&fl=centroide_ll,straatnaam,score" % row[fieldName]
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

                    w = csv.DictWriter(outputFile, row.keys())
                    if header == False:
                        w.writeheader()
                        header = True
                    w.writerow(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get the centroid of streetnames in a city using:\
                                                  https://github.com/PDOK/locatieserver/wiki/API-Locatieserver')
    parser.add_argument('file', help='Add filename location: example/test.csv')
    parser.add_argument('city', help='Add the name of the city, for example: Amsterdam')
    args = parser.parse_args()

    # save api requests to temporary sqlite db for use with many reoccuring names
    requests_cache.install_cache('requests_cache', backend='sqlite')  # , expire_after=180)
    get_centroid_street(args.file, args.city)
