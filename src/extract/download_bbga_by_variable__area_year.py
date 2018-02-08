import pandas as pd
import requests
from sqlalchemy import create_engine
from sqlalchemy.sql import text


def statisticsByAreaByYear(variableName, AreaType, Year):
    """
        Area options: stadsdeel, gebiedsberichtwerken, buurtcombinatie, buurt
        Year options: e.g., 2015, 2016, 2017
        variableNames can be found here: https://api.datapunt.amsterdam.nl/bbga/variabelen/
    """

    # API's
    api_areas = "https://api.data.amsterdam.nl/gebieden/"+ AreaType + "/"
    api_bbga = "https://api.data.amsterdam.nl/bbga/cijfers/"
    api_bbga_meta = "https://api.data.amsterdam.nl/bbga/meta/"

    # Get Area data
    areas = requests.get(url=api_areas).json()['results']

    # Save Area codes and names in dict
    areas_dict = {}
    for i in range(len(areas)):
        code = areas[i]['code']
        naam = areas[i]['naam']
        areas_dict[naam] = code

    # Create DataFrame from Dict
    df_std = pd.DataFrame.from_dict(areas_dict, orient='index')

    # Get the full name of the variable
    bbga_meta = requests.get(url=api_bbga_meta, params={"variabele": variableName})
    fullNameVariable = bbga_meta.json()['results'][0]['label']

    # Get values of each Area by AreaCode
    for key in areas_dict.keys():
        bbga_std = requests.get(url=api_bbga, params={  "format": "json",
                                                        "gebiedcode15": areas_dict[key],
                                                        "jaar": 2017,
                                                        "variabele": variableName})
        value = bbga_std.json()['results'][0]['waarde']
        df_std.loc[key, fullNameVariable] = value

    # Add column names to dataframe:
    df_std = df_std.reset_index()
    df_std.columns = ['stadsdeel', 'stadsdeel_code', fullNameVariable]

    return df_std


def writeStatisticsTable2PGTable(schema, tableName, df_std):
    """
        Change database conenction parameters with your own login credentials and make sure that schema exists
    """

    # Database connection PARAMETERS:
    host = 'localhost'
    port = 5432
    database = 'gisdb'
    user = 'postgres'
    password = 'postgres'
    dialect = 'postgresql'

    db_url = '{dialect}://{user}:{password}@{host}:{port}/{database}'.format(dialect=dialect, user=user, password=password, host=host, port=port, database=database)
    engine = create_engine(db_url)

    # Write dataframe to database:
    df_std.to_sql('d_bbga_cd', con=engine, schema=schema, if_exists='replace')


def main():
    """
        Example using total citizens by department in 2017
        Written to schema 'bi_afval' and table d_bbga_cd'
    """
    data = statisticsByAreaByYear('BEVTOTAAL', 'stadsdeel', 2017)
    writeStatisticsTable2PGTable('bi_afval','d_bbga_cd', data)


if __name__=="__main__":
    main()