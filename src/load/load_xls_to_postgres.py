import os
#import tempfile
import subprocess
import logging
import argparse
from collections import OrderedDict
import configparser

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

import pandas as pd
import pyproj as proj

config = configparser.RawConfigParser()
config.read('auth.conf')

# setup your projections
crs_wgs = proj.Proj(init='epsg:4326') # assuming you're using WGS84 geographic
crs_rd = proj.Proj(init='epsg:28992') # use a locally appropriate projected CRS


FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


class NonZeroReturnCode(Exception):
    pass


# -----------------------------------------------
# Functions
# -----------------------------------------------

def scrub(l):
    out = []
    for x in l:
        if x.strip().startswith('PG:'):
            out.append('PG: <CONNECTION STRING REDACTED>')
        else:
            out.append(x)
    return out


def run_command_sync(cmd, allow_fail=False):
    logging.debug('Running %s', scrub(cmd))
#    logging.debug('Running %s', cmd)
    p = subprocess.Popen(cmd)
    p.wait()

    if p.returncode != 0 and not allow_fail:
        raise NonZeroReturnCode

    return p.returncode


def wfs2psql(url, pg_str, layer_name, **kwargs):
    cmd = ['ogr2ogr','-overwrite','-t_srs', 'EPSG:28992', '-nln', layer_name, '-F', 'PostgreSQL', pg_str, url]
    run_command_sync(cmd)


def get_pg_str(host, port, user, dbname, password):
    return 'PG:host={} port={} user={} dbname={} password={}'.format(
        host, port, user, dbname, password
    )

def esri_json2psql(json_filename, pg_str, layer_name, **kwargs):
    # first attempt:
    # https://gis.stackexchange.com/questions/13029/converting-arcgis-server-json-to-geojson
    cmd = ['ogr2ogr', '-t_srs', 'EPSG:28992', '-nln', layer_name, '-F', 'PostgreSQL', pg_str, json_filename]
    run_command_sync(cmd)


# -----------------------------------------------
# Load FILES or SERVICES
# -----------------------------------------------

def load_gebieden(pg_str):
    areaNames = ['stadsdeel', 'buurt', 'buurtcombinatie', 'gebiedsgerichtwerken']
    srsName = 'EPSG:28992'
    for areaName in areaNames:
        WFS="https://map.data.amsterdam.nl/maps/gebieden?REQUEST=GetFeature&SERVICE=wfs&Version=2.0.0&SRSNAME=" + srsName + "&typename=" + areaName
        wfs2psql(WFS, pg_str , areaName)
        print(areaName + ' loaded into PG.')


def load_crow(datadir, dbConfig):
    # This contains knowledge about the data layout
    #CROW_COLUMNS = OrderedDict([
    #    ('BU_CODE', str),
    #    ('Buurt', str),
    #    ('Kleur', str),
    #])

    # datadir = 'data/aanvalsplan_schoon/crow'
    files = os.listdir(datadir)
    files_xls = [f for f in files if f[-4:] == 'xlsx']
    print(files_xls)

    # Load all files into 1 big dataframe with lat lon as 4326
    df = pd.DataFrame()
    for f in files_xls:
        data = pd.read_excel(datadir + '/' + f)
        if data.empty:
            print('no data')
            continue
        #print('start')
        #print(data.head(1))
        #if ('Schouwronde') not in data.columns:
        #    data['Schouwronde'] = f
        def renameTitles(data, listItems):
            for k,v in listItems.items():
                if k in data.columns:
                    data.rename(columns={k:v}, inplace=True)
            return data
        #if 'Well ID (c' in data.columns:
        #    del data['Well ID (c']
        #if 'Well ID (customer)' in data.columns:
        #    del data['Well ID (customer)']
        list2Replace = {'Aanmaakdatum_score':'Aanmaakdatum score',
                        'Containert': 'Containertype',
                        'Serienumme': 'Serienummer',
                        'Volume con': 'Volume containertype',
                        #'Well ID (c': 'Well ID container',
                        #'XMIN': 'minx',
                        #'XMAX': 'maxx',
                        #'YMAX': 'maxy',
                        #'YMIN': 'miny',
                        #'Latitude': 'lat',
                        #'Longitude': 'lon',
                        'Breedtegraad': 'lat',
                        'Lengtegraad': 'lon',
                        #'Well ID (container)': 'Well ID container',
                        #'Well ID (customer)': 'Well ID customer',
                        #'X':'RD-X',
                        #'Y':'RD-Y'
                        }
        data.rename(columns=lambda x: x.replace("(", '').replace(')', ''), inplace=True)
        data = renameTitles(data, list2Replace)

        #newSet = pd.DataFrame()
        #newSet['Aanmaakdatum score'] = data['Aanmaakdatum score']
        #newSet['Inspecteur'] = data['Inspecteur']
        #newSet['Volgnummer inspectie'] = data['Volgnummer inspectie']
        #newSet['Volgnummer score'] = data['Volgnummer score']
        ##newSet['Score'] = data['Score']
        #if 'maxx' in data.columns:
        #    newSet['maxx'] = data['maxx']
        #    newSet['maxy'] = data['maxy']
        #    newSet['minx'] = data['minx']
        ##    newSet['miny'] = data['miny']
        #if 'lat' in data.columns:
        #    print(data['lat'])
        #    newSet['lat'] = data['lat']
        ##    newSet['lon'] = data['lon']
        #if 'RD-X' in data.columns:
        #    newSet['RD-X'] = data['RD-X']
        #    newSet['RD-Y'] = data['RD-Y']
        #if 'Adres' in data.columns:
        #   newSet['Adres'] = data['Adres']
        #if 'Containertype' in data.columns:
        #    newSet['Containertype'] = data['Containertype']
        #df = df.append(newSet, ignore_index=True)

        df = df.append(data, ignore_index=True)
        print("added " + f)
        #print(df.tail(1))
        #data["Aanmaakdatum score"].apply(pd.to_datetime)
     
        #print(data.columns)

        # convert RD bbox to lat lon, but skip 2014-2017 which is already converted
        #if ('minx') in data.columns and ('lat') not in data.columns:
        #    data['RD-X'] = (data['minx'] + data['maxx']) / 2
        #    data['RD-Y'] = (data['miny'] + data['maxy']) / 2
            #print(data)
            # convert RD N to WGS84 into Series
            #latlon = data.apply(lambda row: proj.transform(crs_rd, crs_wgs, row['RD-X'], row['RD-Y']), axis=1).apply(pd.Series)
            #print(latlon)
            #latlon.rename(columns={0: "lat", 1: "lon"}, inplace=True)
            #print(latlon)
            # Merge with dataFrame
            #data = pd.concat([data,latlon], axis=1)
            #print(data.head())
        
    print(df.columns)
    #df['Aanmaakdatum_score']= df['Aanmaakdatum_score'].apply(pd.to_datetime)
    # Create shapely point object
    #geometry = [Point(xy) for xy in zip(df['lat'], df['lon'])]
    # Convert to lossless binary to load properly into Postgis
    #df['geom'] = geometry.wkb_hex




    LOCAL_POSTGRES_URL = URL(
        drivername='postgresql',
        username=config.get(dbConfig,'user'),
        password=config.get(dbConfig,'password'),
        host=config.get(dbConfig,'host'),
        port=config.get(dbConfig,'port'),
        database=config.get(dbConfig,'dbname')
    )

    # Write our data to database
    tableName = 'crowscores'
    engine = create_engine(LOCAL_POSTGRES_URL)
    df.to_sql(tableName, engine, if_exists='replace') #,  dtype={geom: Geometry('POINT', srid='4326')})
    print(tableName + ' added')



def main(datadir, dbConfig):
    pg_str = get_pg_str(config.get(dbConfig,'host'),config.get(dbConfig,'port'),config.get(dbConfig,'dbname'), config.get(dbConfig,'user'), config.get(dbConfig,'password'))
    
    load_crow(datadir, dbConfig)
    load_gebieden(pg_str)


if __name__ == '__main__':
    desc = 'Upload crow datasets into PostgreSQL.'
    parser = argparse.ArgumentParser(desc)
    parser.add_argument(
        'datadir', type=str, help='Local data directory', nargs=1)
    parser.add_argument(
        'dbConfig', type=str, help='database config settings: dev or docker', nargs=1)
    args = parser.parse_args()

    # Check whether local cached downloads should be used.
    ENV_VAR = 'EXTERNAL_DATASERVICES_USE_LOCAL'
    use_local = True if os.environ.get(ENV_VAR, '') == 'TRUE' else False

    if not use_local:
        main(args.datadir[0], args.dbConfig[0])