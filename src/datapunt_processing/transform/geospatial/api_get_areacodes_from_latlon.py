import requests
from datapunt_processing import logger

logger = logger()


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
        # logger.info(getData.status_code)
        jsonData = getData.json()
        return jsonData
    else:
        return getData.status_code


def getAreaCodes(item, lat, lon):
    """
    Get specific information like area codes based radius to nearest address based on lat/lon value
       ex: https://api.data.amsterdam.nl/geosearch/search/?item=verblijfsobject&lat=52.3731750&lon=4.8924655&radius=50
    It currently is coded to work to get:
    - "buurt"
    - "buurtcombinatie"
    - "stadsdeel"
    """
    if item in ["buurt", "buurtcombinatie", "stadsdeel"]:
        url = "https://api.data.amsterdam.nl/geosearch/search/?item=%s&lat=%s&lon=%s&radius=1" % (item, lat, lon)
        logger.info(url)
        jsonData = getJson(url)
        logger.info(jsonData)

        if "features" in jsonData and len(jsonData["features"]) > 0:
            uri = jsonData["features"][0]["properties"]["uri"]
            data = getJson(uri)
            if item == "buurt" or item == "buurtcombinatie":
                return [data["volledige_code"], data["naam"]]
            if item == "stadsdeel":
                return [data["code"], data["naam"]]
        else:
            logger.info('Valt buiten Amsterdam')
            return None
    else:
        logger.info("Ongeldig item")
        return None


def getAreaCodesforDataFrame(df, item):
    """
    Get specific information like area codes based radius to nearest address based on lat/lon value for each row in pandas DF. 
    Args:
        df with column "lon" and "lat"
        item, which is "buurt", "buurtcombinatie" or "stadsdeel"
    Returns:
        df with two new columns that describe name and code of the item "
    """
    df['code'] = 0
    df['%snaam' % (item)] = 0

    for i in range(len(df)):
        if getAreaCodes(item, df['lat'][i], df['lon'][i]):
            df.loc[i, 'code'], df.loc[i,'%snaam' % (item)] = getAreaCodes(item, df['lat'][i], df['lon'][i])
        else:
            df.loc[i, 'code'], df.loc[i,'%snaam' % (item)] = ["",""]
    return df
