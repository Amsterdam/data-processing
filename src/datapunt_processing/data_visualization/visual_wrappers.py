import matplotlib as mpl
import matplotlib.image as image # for Gemeente logo
import seaborn as sns
import folium
from folium import plugins
import re
import branca.colormap as cm
import requests
import pandas as pd

# bokeh gears
from bokeh.models import BoxZoomTool
from bokeh.plotting import figure, output_notebook, show
from bokeh.tile_providers import STAMEN_TONER, STAMEN_TERRAIN, STAMEN_TONER_BACKGROUND

output_notebook() # for rendering inside jupyter notebook

##################### BOKEH ###############################


# x_range, y_range coordinates for correct Amsterdam WebMercator rendering on maps
AMS = x_range, y_range = ((529158.63554,559679.774276), (6852787.97428,6877562.11813))

plot_width  = int(750)
plot_height = int(plot_width//1.2)


def base_plot(tools='pan,wheel_zoom,reset',plot_width=plot_width, plot_height=plot_height, **plot_args):
    """
    base map of amsterdam for Bokeh interactive plots
    Args:
        tools: default with pan, wheel_zoom and reset. Other options: 'undo', 'redo', 'save'
               'zoom_out', 'zoom_in', 'crosshair', 'hover', 'tap'
        plot_width: width of the plot
        plot_height: height of the plot
        **plot_args: f.i. backgroundcolor, responsive = False/True etc.. 
    Returns:
        baseplot in bokeh (to be rendered in Jupyter Notebook/ Labs
    """
    p = figure(tools=tools, plot_width=plot_width, plot_height=plot_height,
               x_range=x_range, y_range=y_range, outline_line_color=None,
               min_border=0, min_border_left=0, min_border_right=0,
               min_border_top=0, min_border_bottom=0, **plot_args)
    
    p.axis.visible = False
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    
    p.add_tools(BoxZoomTool(match_aspect=True))
    
    return p


################### FOLIUM ##############################

def folium_heatmap(df, lat_col, lon_col, zoom_start=11, \
                plot_points=False, pt_radius=15, popup_name = 'subrubriek' , \
                draw_heatmap=False, heat_map_weights_col=None, \
                heat_map_weights_normalize=True, heat_map_radius=15):
    """Creates a Folium heatmap with a dataframe of lat lon points. Can also produce a 
    heatmap overlay. 
    Note: pop_name arg is set to 'subrubriek', only present in Mora dataset

    Arg:
        df: dataframe lon lat coordinates to maps
        lat_col: Column containing latitude
        lon_col: Column containing longitude
        zoom_start: initial zoom of the map
        plot_points: Add points to map (boolean)
        popup_name = When adding points this will be the pop_up name (choose categorical)
        pt_radius: Size of each point
        draw_heatmap: Add heatmap to map (boolean)
        heat_map_weights_col: Column containing heatmap weights
        heat_map_weights_normalize: Normalize heatmap weights (boolean)
        heat_map_radius: Size of heatmap point

    Returns:
        folium map object
    """

    ## center map in the middle of points center in
    middle_lat = df[lat_col].median()
    middle_lon = df[lon_col].median()

    curr_map = folium.Map(location=[middle_lat, middle_lon], tiles='stamentoner', 
                          zoom_start=zoom_start)

    # add points to map
    if plot_points:
        for _, row in df.iterrows():
            folium.CircleMarker([row[lat_col], row[lon_col]],
                                radius=pt_radius,
                                popup=row[popup_name],
                                fill=True,
                                fill_color="red", 
                                fill_opacity=0.7
                               ).add_to(curr_map)

    # add heatmap
    if draw_heatmap:
        # convert to (n, 2) or (n, 3) matrix format
        if heat_map_weights_col is None:
            cols_to_pull = [lat_col, lon_col]
        else:
            # if we have to normalize
            if heat_map_weights_normalize:
                df[heat_map_weights_col] = \
                    df[heat_map_weights_col] / df[heat_map_weights_col].sum()

            cols_to_pull = [lat_col, lon_col, heat_map_weights_col]

        stations = df[cols_to_pull].as_matrix().tolist()
        curr_map.add_child(plugins.HeatMap(stations, radius=heat_map_radius))

    return curr_map


    

def create_map(df, geotype, output_name):
    """
    Create a choropleth map of stadsdelen, gebieden, buurtcombi's or buurten
    Args:
        -df, contains at least:
            - ID (with the code of stadsdeel, gebied, buurtcombinatie or buurt)
            - Value
        - geotype (string): stadsdeel, gebied, buurtcombinatie, buurt
        - output_name (string): name of output file
    returns:Ouput: html with data on map

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
    
    
def create_popup_map(df, output_name, save = None):
    """
    Creates a map with pop-up markers
    Args:
        df: contains at least:
            Name (string with name of datapoint)
            Value (value for this datapoint) 
            lon 
            lat
        output_name (string): how do you want te file to be saved
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
        if row['lon']== 0:
            pass
        else:
            html = u"<b> Naam: </b> {} <br> <b> Waarde: </b> {} <br>".format(row['Name'], row['Value'])  
            html = re.sub(r"'", '&#39;', html) #replace ' with &#39 to prevent error (ASCII code)
            folium.Marker([row['lat'], row['lon']], popup = html).add_to(m)

    if save:
        m.save('{}.html'.format(output_name))
        print('Popup map is succesfully saved as:' + output_name)
    
    return m