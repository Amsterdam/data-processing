import re
import folium
import branca.colormap as cm
import requests
import pandas as pd

def create_map(df, geotype, output_name):
    """
    Input:
        - df, contains at least:
            - ID (with the code of stadsdeel, gebied, buurtcombinatie or buurt)
            - Value
        - geotype (string):
            - stadsdeel
            - gebied
            - buurtcombinatie
            - buurt
        - output_name (string): how do you want te file to be saved
    Ouput: html with data on map

    """
    if geotype not in ['buurtcombinatie', 'gebied', 'buurt', 'stadsdeel']:
        print(
        "geotype wordt niet ondersteund. Kies een vande volgende opties: 'buurtcombinatie', 'gebied', 'buurt' of 'stadsdeel'.")
        return

    if bool(re.search(r"\W", output_name)):
        print("ongeldige outputnaam, outputnaam mag alleen letters, cijfers of _ bevatten")
        return

    if not "ID" in df.columns or not "Value" in df.columns:
        print("dataframe moet 'ID' en 'Value' bevatten")
        return

    if geotype == 'buurtcombinatie':
        response = requests.get(
            'http://maps.amsterdam.nl/open_geodata/geojson.php?KAARTLAAG=GEBIED_BUURTCOMBINATIES&THEMA=gebiedsindeling')
        geo_json_data = response.json()
    elif geotype == 'gebied':
        response = requests.get(
            'http://maps.amsterdam.nl/open_geodata/geojson.php?KAARTLAAG=GEBIEDEN22&THEMA=gebiedsindeling')
        geo_json_data = response.json()
    elif geotype == 'buurt':
        response = requests.get(
            'http://maps.amsterdam.nl/open_geodata/geojson.php?KAARTLAAG=GEBIED_BUURTEN&THEMA=gebiedsindeling')
        geo_json_data = response.json()
    elif geotype == 'stadsdeel':
        response = requests.get(
            'http://maps.amsterdam.nl/open_geodata/geojson.php?KAARTLAAG=GEBIED_STADSDELEN&THEMA=gebiedsindeling')
        geo_json_data = response.json()

    # set colormap
    linear = cm.LinearColormap(['#E5F2FC', '#B1D9F5', '#71BDEE', '#00a0e6', '#004699'])

    colormap = linear.scale(
        df.Value.min(),
        df.Value.max())

    # convert df to dict
    df_dict = df.set_index('ID')['Value']

    # make map
    m = folium.Map(location=[52.379189, 4.899431], tiles='https://{s}.data.amsterdam.nl/topo_google/{z}/{x}/{y}.png',
                   attr='Amsterdam', zoom_start=13, min_lat=52.269470,
                   max_lat=52.4322, min_lon=4.72876, max_lon=5.07916, subdomains=['t1', 't2', 't3', 't4'])

    # plot data on map
    folium.GeoJson(geo_json_data, style_function=lambda feature: {
        'fillColor': colormap(df_dict[feature['properties']['Buurtcombinatie_code']]),
        'color': 'black',
        'weight': 2,
        'dashArray': '5, 5',
        'fillOpacity': 0.9
    }).add_to(m)

    # add scale to map
    colormap.caption = 'Color scale'
    colormap.add_to(m)

    # save map
    m.save('%s.html' % output_name)
    m
    print("kaart is succesvol opgeslagen")
