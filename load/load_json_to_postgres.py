import os
import subprocess
import logging
import argparse
import configparser
import json

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

import pandas as pd
from pandas.io.json import json_normalize
#from shapely.geometry import Point
#from shapely.geometry import wkb_hex
import pyproj as proj

config = configparser.RawConfigParser()
config.read('config.ini')

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


def load_containers(datadir, dbConfig):

    # datadir = 'data/aanvalsplan_schoon/crow'
    files = os.listdir(datadir)
    files_json = [f for f in files if f[-4:] == 'json']
    print(files_json)

    # Load all files into 1 big dataframe with lat lon as 4326
    df = pd.DataFrame()
    for fileName  in files_json:
        with open('data/'+fileName,'r') as response:
            data = json.loads(response.read())
            objectKeyName = list(data[0].keys())[0]
            print(fileName + " object opened")
            data = [item[objectKeyName] for item in data]
            #print(data[0])
            df = json_normalize(data)
            #print(df.head())
            # Create shapely point object
            #geometry = [Point(xy) for xy in zip(df['location.position.latitude'], df['location.position.longitude'])]
            # Convert to lossless binary to load properly into Postgis
            #df['geom'] = geometry.wkb_hex
            print("DataFrame " + objectKeyName + " created")
            LOCAL_POSTGRES_URL = URL(
                drivername='postgresql',
                username=config.get(dbConfig,'user'),
                password=config.get(dbConfig,'password'),
                host=config.get(dbConfig,'host'),
                port=config.get(dbConfig,'port'),
                database=config.get(dbConfig,'dbname')
            )

            # Write our data to database
            tableName = fileName[0:-5]
            engine = create_engine(LOCAL_POSTGRES_URL)
            df.to_sql(tableName, engine, if_exists='replace') #,  dtype={geom: Geometry('POINT', srid='4326')})
            print(tableName + ' added to Postgres')



def main(datadir, dbConfig):
    pg_str = get_pg_str(config.get(dbConfig,'host'),config.get(dbConfig,'port'),config.get(dbConfig,'dbname'), config.get(dbConfig,'user'), config.get(dbConfig,'password'))
    
    load_containers(datadir, dbConfig)
    #load_gebieden(pg_str)


if __name__ == '__main__':
    desc = 'Upload container jsons into PostgreSQL.'
    parser = argparse.ArgumentParser(desc)
    parser.add_argument(
        'datadir', type=str, help='Local data directory', nargs=1)
    parser.add_argument(
        'dbConfig', type=str, help='database config settings: dev or docker', nargs=1)
    args = parser.parse_args()

    main(args.datadir[0], args.dbConfig[0])