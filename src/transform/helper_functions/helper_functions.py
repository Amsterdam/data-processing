


def lonlat_to_meters(df, lon_column, lat_column):
    """
    Convert longitude, latitude GPS coordinates into meters west and north of Greenwich (Web Mercator format). This makes it easier to overlay those with tiles from map providers.
    args:
        df: pandas Dataframe
        lon_name: dataframe column where the longitude coordinates are stored
        lat_name: dataframe column where the latitude coordinates are stored
    example:
        lonlat_to_meters(df, 'lon', 'lat')
        df.rename(columns={'lon':'x', 'lat':'y'}, inplace=True)
    returns:
        df with converted coordinates
    """
    lat = df[lat_column]
    lon = df[lon_column]
    origin_shift = 2 * np.pi * 6378137 / 2.0
    mx = lon * origin_shift / 180.0
    my = np.log(np.tan((90 + lat) * np.pi / 360.0)) / (np.pi / 180.0)
    my = my * origin_shift / 180.0
    df.loc[:, lon_column] = mx
    df.loc[:, lat_column] = my
    
    return df
