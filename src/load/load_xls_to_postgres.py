import os
#import tempfile
import subprocess
import logging
import argparse
from collections import OrderedDict

import pandas as pd
import pyproj as proj

from helper_functions import postgres_engine_pandas

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


def get_pg_str(host, port, user, dbname, password):
    return 'PG:host={} port={} user={} dbname={} password={}'.format(
        host, port, user, dbname, password
    )


# -----------------------------------------------
# Load FILES or SERVICES
# -----------------------------------------------


def load_xls(datadir, tablename, config_path, db_config_name):
    files = os.listdir(datadir)
    files_xls = [f for f in files if f[-4:] == 'xlsx']
    print(files_xls)

    # Load all files into 1 big dataframe with lat lon as 4326
    df = pd.DataFrame()
    for filename in files_xls:
        data = pd.read_excel(datadir + '/' + filename)
        if data.empty:
            print('no data')
            continue

        df = df.append(data, ignore_index=True)
        print("added " + filename)
        #print(df.tail(1))
        #data["Aanmaakdatum score"].apply(pd.to_datetime)

        #if ('minx') in data.columns and ('lat') not in data.columns:
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

        # load the data into pg
        engine = postgres_engine_pandas(config_path, db_config_name)
        # TODO: link to to_sql function
        df.to_sql(filename[-4:], engine, if_exists='replace', index=True, index_label='idx')  # ,dtype={geom: Geometry('POINT', srid='4326')})
        print(filename + ' added')


def parser():
    desc = 'Upload xls files into PostgreSQL using Pandas.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        'datadir', type=str, help='Local data directory, for example: projectdir/data')
    parser.add_argument(
        'tablename', type=str, help='Write the desired table name in lowercase and underscores.')
    parser.add_argument(
        'config_path', type=str, help='Location of the config.ini file: for example: /auth/config.ini')
    parser.add_argument(
        'dbconfig', type=str, help='config.ini name of db settings: dev or docker')
    return parser



def main():
    args = parser().parse_args()
    load_xls(args.datadir, args.tablename, args.config_path, args.dbconfig)


if __name__ == '__main__':
    main()
