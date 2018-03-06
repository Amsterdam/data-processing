import requests

def get_openbareruimte(lat, lon):
    """
    Get the name the street location where it coordinate resides on.

    Args:
        1. lat: 52.3729378
        2. lon:  4.8937806

    Result:
        Returns dictionary of the openbare ruimte object
    """

    parameters = {"lat": lat,
                  "lon": lon,
                  "item": "openbareruimte"
                  }

    url_openbareruimte = "https://api.data.amsterdam.nl/geosearch/search/"

    openbareruimte_data = requests.get(url_openbareruimte, params=parameters).json()

    print(openbareruimte_data)

    # Get lower level objects before the areatype objects like Landelijk gebied'
    for feature in openbareruimte_data["features"]:
        if feature["properties"]["opr_type"] in ('weg', 'terrein', 'kunstwerk', 'water'):
            openbareruimte = feature["properties"]
        else:
            openbareruimte = feature["properties"]

    return openbareruimte


def get_address_near_point(lat, lon, radius):
    """
    Get nearest addres and housenumber based on location.

    ``get_address_near_point(52.3729378, 4.8937806, 50)``

    Args:
        1. lat: 52.3729378
        2. lon:  4.8937806
        3. radius: 50

    Returns:
        Dictionary of the first found address with openbareruimte, huisnummer, postcode, etc...
    """
    lat = str(lat)
    lon = str(lon)
    radius = str(radius)
    openbareruimte = get_openbareruimte(lat, lon)

    url_nummeraanduiding = "https://api.data.amsterdam.nl/bag/nummeraanduiding/"

    parameters = {"locatie": "{}, {}, {}".format(lat, lon, radius),
                  "openbareruimte": openbareruimte["id"],
                  "page_size": 5,
                  "detailed": 1
                  }

    address = requests.get(url_nummeraanduiding, params=parameters).json()

    print(address["results"][0])
    return(address["results"][0])
