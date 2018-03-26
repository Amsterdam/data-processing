import folium
import pandas as pd
import re

def create_popup_map(df, output_name):
    """
    Input:
        - df, contains at least:
            - Name (string with name of datapoint)
            - Value (value for this datapoint)
            - lon
            - lat

        - output_name (string): how do you want te file to be saved
    Ouput: html with data on map

    """

    if bool(re.search(r"\W", output_name)):
        print("ongeldige outputnaam, outputnaam mag alleen letters, cijfers of _ bevatten")
        return

    if not "Name" in df.columns or not "Value" in df.columns or not "lon" in df.columns or not "lat" in df.columns:
        print("dataframe moet 'Name','Value', 'lon' en 'lat' bevatten")
        return

    m = folium.Map(location=[52.379189, 4.899431], tiles='https://{s}.data.amsterdam.nl/topo_google/{z}/{x}/{y}.png',
                   attr='Amsterdam', zoom_start=13, min_lat=52.269470,
                   max_lat=52.4322, min_lon=4.72876, max_lon=5.07916, subdomains=['t1', 't2', 't3', 't4'])

    for index, row in df.iterrows():
        if row['lon'] == 0:
            pass
        else:
            html = u"<b> Naam: </b> {} <br> <b> Waarde: </b> {} <br>".format(row['Name'], row['Value'])
            html = re.sub(r"'", '&#39;', html)
            folium.Marker([row['lat'], row['lon']], popup=html).add_to(m)

    m.save('{}.html'.format(output_name))
    m
    print('Popup map is succesfully saved as:' + output_name)
