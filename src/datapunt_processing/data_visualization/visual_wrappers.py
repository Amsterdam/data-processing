import matplotlib as mpl
import matplotlib.image as image # for Gemeente logo
import seaborn as sns
import folium
from folium import plugins
from bokeh.models import BoxZoomTool
from bokeh.plotting import figure, output_notebook, show

output_notebook()

# x_range, y_range coordinates for correct Amsterdam WebMercator rendering on maps
AMS = x_range, y_range = ((529158.63554,559679.774276), (6852787.97428,6877562.11813))

plot_width  = int(750)
plot_height = int(plot_width//1.2)


def base_plot(tools='pan,wheel_zoom,reset',plot_width=plot_width, plot_height=plot_height, **plot_args):
    p = figure(tools=tools, plot_width=plot_width, plot_height=plot_height,
        x_range=x_range, y_range=y_range, outline_line_color=None,
        min_border=0, min_border_left=0, min_border_right=0,
        min_border_top=0, min_border_bottom=0, **plot_args)
    
    p.axis.visible = False
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    
    p.add_tools(BoxZoomTool(match_aspect=True))
    
    return p



def folium_heatmap(df, lat_col, lon_col, zoom_start=11, \
                plot_points=False, pt_radius=15, popup_name = 'subrubriek' , \
                draw_heatmap=False, heat_map_weights_col=None, \
                heat_map_weights_normalize=True, heat_map_radius=15):
    """Creates a Foilium HeatMap given a dataframe of lat lon points. Can also produce a 
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

    
