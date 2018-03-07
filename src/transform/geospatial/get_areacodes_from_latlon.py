def getJson(url):
    """
    Get a json from an url

    Args:
        url: give an api url::

            https://api.data.amsterdam.nl/bag/gebieden/stadsdeel
    Returns:
        a parsed json result or an error message
    """
    getData = requests.get(url)
    if getData.status_code == 200:
        # print(getData.status_code)
        jsonData = getData.json()
        return jsonData
    else:
        return print(getData.status_code)


def getAreaCodes(item, lat, lon):
    """
    Get specific information like area codes based radius to nearest address based on lat/lon value
       ex: https://api.data.amsterdam.nl/geosearch/search/?item=verblijfsobject&lat=52.3731750&lon=4.8924655&radius=50
    It currently is coded to work only to get buurten
    """
    url = "https://api.data.amsterdam.nl/geosearch/search/?item=%s&lat=%s&lon=%s&radius=1" % (item, lat, lon)
    print(url)
    jsonData = getJson(url)
    print(jsonData)

    if jsonData["features"]:
        uri = jsonData["features"][0]["properties"]["uri"]
        data = getJson(uri)
        # print(data['volledige_code'])
        return [data["buurt"]["code"], data["buurt"]["naam"]]
    else:
        print('Valt buiten Amsterdamse buurten')
        return ['Valt niet binnen buurt', 'Buiten Amsterdam']
