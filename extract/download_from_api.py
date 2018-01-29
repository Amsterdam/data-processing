# utf-8
import requests
import json
import csv
import os

from getaccesstoken import GetAccessToken


def pretty_json(response):
    print(json.dumps(response.json(), indent=4))


def getJsonPage(accessToken, page):
    response = requests.get(url, headers=accessToken, params={'page': page})
    return response


def getLengthCategory():
    url = "https://api.data.amsterdam.nl/tellus/lengtecategorie/"
    jsonLengthCategory = getJsonData(url)
    return jsonLengthCategory["_embedded"][0]


def getSpeedCategory():
    url = "https://api.data.amsterdam.nl/tellus/snelheidscategorie/"
    jsonSpeedCategory = getJsonData(url)
    return jsonSpeedCategory["_embedded"][0]


def getTellus():
    getToken = GetAccessToken()  # Create instance of class
    accessToken = getToken.getAccessToken()  # Get Access token

    url = "https://api.data.amsterdam.nl/tellus/tellus"
    response = requests.get(url, headers=accessToken)
    jsonTellus = response.json()
    return jsonTellus["_embedded"]


def conversionListCvalues():
    # Create conversion table for matrix c1-c60
    lCategorie = getLengthCategory()
    sCategorie = getSpeedCategory()
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


def getJsonData(url):
    getToken = GetAccessToken()  # Create instance of class
    accessToken = getToken.getAccessToken()  # Get Access token
    response = requests.get(url, headers=accessToken)  # Get first page for count
    jsonData = response.json()
    return jsonData


def getRowCount(csvFile):
    with open(csvFile, "r") as File:
        reader = csv.reader(File, delimiter=',')
        print('Getting number of rows of CSV file')
        data = list(reader)
        print(len(data))
        return len(data)


def hasHeader(csvFile):
    with open(csvFile, 'r') as csvfile:
        sniffer = csv.Sniffer()
        has_header = sniffer.has_header(csvfile.read(2048))
        csvfile.seek(0)
        print(has_header)
        return has_header  # true or false


def reformatData(item):

    newRow = {}  # Create empty dict for row key, values
    reusingItem = {}  # Create dict with same data for each c value

    for k, v in item.items():  # fill dict with same value data
        if k[:1] != 'c':
            reusingItem[k] = v

    # Add tellus information by id
    tellusId = item["tellus"].split("/")[-2]
    for tellus in Tellussen:
        if int(tellus["id"]) == int(tellusId):
            reusingItem.update(tellus)

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
    #print(reusingItem)

    # Create 60 rows by c-waarde
    for key, value in item.items():
        # Add basic values for c-waarde and tellus info
        if key[:1] == 'c':
            newRow['c_waarde'] = key
            newRow['meetwaarde'] = value
            # add length & speed ids
            for k, v in cValues.items():
                if k == key:
                    newRow['lengte_interval'] = v[0]
                    newRow['snelheids_interval'] = v[2]
            newRow.update(reusingItem)
    return newRow


# Initial variables
fileName = "tellusdata.csv"
url = "https://api.data.amsterdam.nl/tellus/tellusdata/"
cValues = conversionListCvalues()
Tellussen = getTellus()
getToken = GetAccessToken()  # Create instance of class
accessToken = getToken.getAccessToken()  # Get Access token



with open(fileName, "a", newline='') as csvFile:
    # Check if File is empty, if so then use initial data
    if os.stat(fileName).st_size == 0:        
        startPage = 1
        hasHeader = False
    else:
        # Check exisiting csv file for startPage and if header exists
        hasHeader = hasHeader(fileName)
        rows = getRowCount(fileName)
        startPage = int(abs(((rows - 1) / 60) / 100)) # c = 60 rows and 100 per page
        print(startPage)

    # Setup writer
    csvWriter = csv.writer(csvFile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    # Get number of pages to loop over
    firstPage = getJsonData(url)
    numberOfPages = int(abs(firstPage['count'] / 100))
    print(numberOfPages)

    for page in range(startPage, numberOfPages):
        response = getJsonPage(accessToken, page)
        # print('status: ' + str(response.status_code))

        if response.status_code != 200:
            accessToken = getToken.getAccessToken()
            response = getJsonPage(accessToken, page)
            if response.status_code != 200:
                print('Error status: ' + str(response.status_code))
                break

        jsonData = response.json()

        data = jsonData['_embedded']
        for item in data:
            newRow = reformatData(item)

            # Create header if not present
            if hasHeader == False:
                header = list(newRow.keys())
                #print(header)
                csvWriter.writerow(header)
                hasHeader = True
            # Add c-waarde row
            values = list(newRow.values())
            csvWriter.writerow(values)

        # data['tellusdata'].extend(jsonData['_embedded'])
        # json.dump(data, outputFile, indent=4, sort_keys=True)
        print('Page ' + str(startPage) + ' of ' + str(numberOfPages))
        startPage += 1