import requests
import pandas as pd

def adress_to_latlon(df):
    """
    This function adds the lattitude and longtitude to a pandas df based on an adress.

    input:
    pandas df met tenminste de volgende variabelen:
        - Straat: String met de naam van de straat
        - Huisnr: String met huisnummer
    output:
    pandas df waaraan de volgende variabelen zijn toegevoegd:
        - lon: longtitude behorend bij adres
        - lat: lattitude behorend bij adres
    """
    lon = []
    lat = []

    for index, row in df.iterrows():
        url = u'https://api.data.amsterdam.nl/atlas/search/adres/?q={} {}'.format(row['Straat'], row['Huisnr'])
        response = requests.get(url)
        if len(response.json()['results']) == 0:  # het adres kan niet worden gevonden
            lon.append(0)
            lat.append(0)
        else:
            lon.append(response.json()['results'][0]['centroid'][0])
            lat.append(response.json()['results'][0]['centroid'][1])

    df['lon'] = lon
    df['lat'] = lat

    return df