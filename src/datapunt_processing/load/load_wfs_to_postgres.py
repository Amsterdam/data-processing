#!/usr/bin/env python3

import subprocess
import argparse

from datapunt_processing import logger
from datapunt_processing.helpers.connections import psycopg_connection_string

# Setup basic logging
logger = logger()


class NonZeroReturnCode(Exception):
    """Used for subprocess error messages."""
    pass


def scrub(line):
    """Hide the login credentials of Postgres in the console."""
    out = []
    for x in line:
        if x.strip().startswith('PG:'):
            out.append('PG: <CONNECTION STRING REDACTED>')
        else:
            out.append(x)
    return out


def run_command_sync(cmd, allow_fail=False):
    """
    Run a string in the command line.

    Args:
        1. cmd: command line code formatted as a list::

            ['ogr2ogr', '-overwrite', '-t_srs', 'EPSG:28992','-nln',layer_name,'-F' ,'PostgreSQL' ,pg_str ,url]

        2. Optional: allow_fail: True or false to return error code

    Returns:
        Excuted program or error message.
    """
    # logger.info('Running %s', scrub(cmd))
    p = subprocess.Popen(cmd)
    p.wait()

    if p.returncode != 0 and not allow_fail:
        raise NonZeroReturnCode

    return p.returncode


def wfs2psql(url, pg_str, layer_name, **kwargs):
    """Command line ogr2ogr string to load a WFS into PostGres."""
    cmd = ['ogr2ogr', '-overwrite', '-t_srs', 'EPSG:28992','-nln',layer_name,'-F' ,'PostgreSQL' ,'PG:'+pg_str ,url]
    run_command_sync(cmd)


def load_layers(pg_str):
    """
    Load layers into Postgres using a list of titles of each layer within the WFS service.

    Args:
        pg_str: psycopg2 connection string::

        'PG:host= port= user= dbname= password='

    Returns:
        Loaded layers into postgres using ogr2ogr.

    """
    layerNames = ['stadsdeel',
                  'buurt',
                  'buurtcombinatie',
                  'gebiedsgerichtwerken']

    srsName = 'EPSG:28992'

    for areaName in layerNames:
        WFS = "https://map.data.amsterdam.nl/maps/gebieden?REQUEST=GetFeature&SERVICE=wfs&Version=2.0.0&SRSNAME=" + srsName + "&typename=" + areaName
        wfs2psql(WFS, pg_str, areaName)
        logger.info(areaName + ' loaded into PG.')


def parser():
    """Parser function to run arguments from commandline and to add description to sphinx."""
    desc = """
    Upload gebieden into PostgreSQL from the WFS service of api.data.amsterdam.nl with use of ogr2ogr.

    Add ogr2ogr path ENV if running locally in a virtual environment:
        ``export PATH=/Library/Frameworks/GDAL.framework/Programs:$PATH``

    Example command line:
        ``load_wfs_to_postgres config.ini dev``
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        'config_path', type=str, help="Type the relative path + name of the config file, for example: auth/config.ini")
    parser.add_argument(
        'db_config', type=str, help="Type 'dev' or 'docker' to load the proper port and ip settings in the config file")
    return parser


def main():
    args = parser().parse_args()
    db_config = args.db_config[0]
    pg_str = psycopg_connection_string(args.config_path, args.db_config)
    load_layers(pg_str)


if __name__ == '__main__':
    main()
