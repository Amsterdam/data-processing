# utf-8
import argparse
import requests
import requests_cache
import json
import os

from authentication.getaccesstoken import GetAccessToken
from helpers.files import save_file


def conversionListCvalues(metadata):
    # Create conversion table for matrix c1-c60
    lCategorie = metadata["lengtecategorie"]["_embedded"][0]
    sCategorie = metadata["snelheidscategorie"]["_embedded"][0]
    cValues = {}
    cNumber = 1
    while cNumber <= 60:  # c1 to c60 colums
        length = 1
        while length <= 6:  # 6 length types x
            speed = 1
            while speed <= 10:  # 10 speed types
                cValue = 'c' + str(cNumber)
                lValue = 'l' + str(length)
                for key, value in lCategorie.items():
                    if lValue == key:
                        lName = value
                sValue = 's' + str(speed)
                cValues.update({cValue: [lValue, lName, sValue]})
                # print('c'+str(length)+', ' + str(length) + ', '+ str(speed))
                speed += 1
                cNumber += 1
            length += 1
    return cValues


def getJsonData(url, accessToken):
    response = requests.get(url, headers=accessToken)  # Get first page for count
    if response.status_code != 200:
        if response.status_code == 404 or response.status_code == 401:
            print('Error status: {} {}'.format(str(response.status_code), "trying with trailing / ..."))
            response = requests.get(url + '/', headers=accessToken)
        else:
            return print('Error status: ' + str(response.status_code))
    jsonData = response.json()
    print("recieved data from {} ".format(url))
    return jsonData


def reformatData(item, tellus_metadata, cvalues):
    newRow = {}  # Create empty dict for row key, values
    reusingItem = {}  # Create dict with same data for each c value
    #print(item)
    for k, v in item.items():  # fill dict with same value data
        if k[:1] != 'c':
            reusingItem[k] = v

    # Add tellus information by id
    tellus_id = int(item["tellus"].split("/")[-2])

    for tellus_details in tellus_metadata:
        if int(tellus_details["id"]) == tellus_id:
            reusingItem.update(tellus_details)

    # Remove api uri's and other non usable items for Tableau
    reusingItem['snelheids_klasse'] = reusingItem['snelheids_klasse'].split("/")[-2]
    reusingItem.pop('_display')
    reusingItem.pop('lengte_categorie')
    reusingItem.pop('snelheids_categorie')
    reusingItem.pop('tellus')
    reusingItem.pop('geometrie')
    reusingItem.pop('rijksdriehoek_x')
    reusingItem.pop('rijksdriehoek_y')
    reusingItem.pop('dataset')

    # Create 60 rows by c-waarde
    for key, value in item.items():
        # Add basic values for c-waarde and tellus info
        if key[:1] == 'c':
            newRow['c_waarde'] = key
            newRow['meetwaarde'] = value
            # add length & speed ids
            for k, v in cvalues.items():
                if k == key:
                    newRow['lengte_interval'] = v[0]
                    newRow['snelheids_interval'] = v[2]
            newRow.update(reusingItem)
    return newRow


def get_data(url_api, endpoint, metadata, accessToken, limit):
    data = []
    url = url_api + '/' + endpoint
    startPage = 1
    has_next_key = False
    nextKey = ""
    cvalues = conversionListCvalues(metadata)
    json_data = getJsonData(url, accessToken)

    number_of_items = json_data['count']
    print("number of items {}".format(number_of_items))
    number_of_pages = int(abs(number_of_items/100))

    if "next" in json_data["_links"].keys():
        has_next_key = True
        url = json_data["_links"]["next"]
        print(url)
    while has_next_key and startPage < limit:
        response = getJsonData(url, accessToken)
        if "next" in response["_links"].keys():
            url = response["_links"]["next"]
            print(nextKey)
        else:
            has_next_key = False
            # no next_key, stop the loop
        # print('status: ' + str(response.status_code))

        for item in response["_embedded"]:
            #print(item)
            newRow = reformatData(item, metadata['tellus']['_embedded'], cvalues)
            # Add c-waarde row
            #values = list(newRow.values())
            # append to main data array
            data.append(newRow)
        # json.dump(data, outputFile, indent=4, sort_keys=True)
        print('Page {} of {}'.format(startPage,number_of_pages))
        startPage += 1
    #print(data)
    return data



def parser():
    """Parser function to run arguments from commandline and to add description to sphinx docs."""
    description = """
    Download from an API from data.amsterdam.nl through the OAuth2 datapunt Authorization service:
    `download_from_data_amsterdam_api https://api.data.amsterdam.nl/tellus data tellusdata.csv 10`
    """

    parser = argparse.ArgumentParser(
                        description=description)
    parser.add_argument('url',
                        type=str,
                        help='add full endpoint, for example https://api.data.amsterdam.nl/tellus/')
    parser.add_argument('output_folder',
                        type=str,
                        help='add outputfolder location, for example my_project_folder/data or . if you want to save in the current dir')
    parser.add_argument('filename',
                        type=str,
                        help='add filename for example tellusdata.csv')
    parser.add_argument('limit',
                        type=int,
                        help='add limited number of pages to test outputfile')
    return parser


def main():
    # Return all arguments in a list
    args = parser().parse_args()
    print("Getting Access token.")
    #getToken = GetAccessToken()  # Create instance of class
    accessToken = GetAccessToken().getAccessToken()
    print("Setup temp database to store requests to speed up restart download if network fails.")
    requests_cache.install_cache('requests_db', backend='sqlite')

    endpoints = ['tellus', 'snelheidscategorie', 'lengtecategorie']
    metadata = {}
    for endpoint in endpoints:
        json_data = getJsonData(args.url + '/' + endpoint, accessToken)
        # print(json_data)
        metadata.update({endpoint: json_data})
        print("retrieved {}".format(endpoint))
    data = get_data(args.url, 'tellusdata', metadata, accessToken, args.limit)
    save_file(data, args.output_folder, args.filename)


if __name__ == "__main__":
    main()
