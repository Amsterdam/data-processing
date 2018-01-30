def getJson(url):
    getData = requests.get(url)
    if getData.status_code == 200:
        # print(getData.status_code)
        jsonData = getData.json()
        return jsonData
    else:
        return print(getData.status_code)


def getAreaCodes(item, key, lat, lon):
    """
    Get specific information like area codes based radius to nearest address based on lat/lon value
       ex: https://api.data.amsterdam.nl/geosearch/search/?item=verblijfsobject&lat=52.3731750&lon=4.8924655radius=50
    """
    url = "https://api.data.amsterdam.nl/geosearch/search/?item=%s&lat=%s&lon=%s&radius=1" % (item, lat, lon)
    print(url)
    jsonData = getJson(url)
    print(jsonData)

    if jsonData["features"]:
        uri = jsonData["features"][0]["properties"]["uri"]
        data = getJson(uri)
        # print(data['volledige_code'])
        return [data[key], data["stadsdeel"]["naam"]]
    else:
        print('Valt buiten Amsterdamse buurten')
        return ['Valt niet binnen buurt', 'Buiten Amsterdam']
