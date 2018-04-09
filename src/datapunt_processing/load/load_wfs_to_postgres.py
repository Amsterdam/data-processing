#!/usr/bin/env python3

import subprocess
import argparse
from urllib.parse import urlencode
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


def load_wfs_layer_into_postgres(pg_str, url_wfs, layer_name, srs, retry_count=3):
    """
    Get layer from a wfs service.
    Args:
        1. url_wfs: full url of the WFS including https, excluding /?::

            https://map.data.amsterdam.nl/maps/gebieden

        2. layer_name: Title of the layer::

            stadsdeel

        3. srs: coordinate system number, excluding EPSG::

            28992

    Returns:
        The layer loaded into postgres
    """  # noqa

    parameters = {
        "REQUEST": "GetFeature",
        "TYPENAME": layer_name,
        "SERVICE": "WFS",
        "VERSION": "2.0.0",
        #"SRSNAME": "EPSG:{}".format(srs)
    }

    logger.info("Requesting data from {}, layer: {}".format(
        url_wfs, layer_name))
    url = url_wfs + '?' + urlencode(parameters)
    srs = "EPSG:{}".format(srs)
    cmd = ['ogr2ogr', '-overwrite', '-t_srs', srs, '-nln', layer_name, '-F', 'PostgreSQL', 'PG:'+pg_str, url]
    run_command_sync(cmd)


def load_wfs_layers_into_postgres(config_path, db_config, url_wfs, layer_names, srs_name):
    """
    Load layers into Postgres using a list of titles of each layer within the WFS service.

    Args:
        pg_str: psycopg2 connection string::

        'PG:host= port= user= dbname= password='

    Returns:
        Loaded layers into postgres using ogr2ogr.

    """
    pg_str = psycopg_connection_string(config_path, db_config)

    layers = layer_names.split(',')
    logger.info('Layers:',layers)

    for layer_name in layers:
        load_wfs_layer_into_postgres(pg_str, url_wfs, layer_name, srs_name)
        logger.info(layer_name + ' loaded into PG.')


def parser():
    """Parser function to run arguments from commandline and to add description to sphinx."""
    desc = """
    Upload gebieden into PostgreSQL from the WFS service with use of ogr2ogr.

    Add ogr2ogr path ENV if running locally in a virtual environment:
        ``export PATH=/Library/Frameworks/GDAL.framework/Programs:$PATH``

    Example command line:
        ``load_wfs_to_postgres config.ini dev https://map.data.amsterdam.nl/maps/gebieden 
          stadsdeel,buurtcombinatie,gebiedsgerichtwerken,buurt 28992``
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        'config_path',
        type=str,
        help="Type the relative path + name of the config file, for example: auth/config.ini")
    parser.add_argument(
        'db_config',
        type=str,
        help="Type 'dev' or 'docker' to load the proper port and ip settings in the config file")
    parser.add_argument(
        'url',
        type=str,
        help="""
        Url of the WFS service, for example:
        https://map.data.amsterdam.nl/maps/gebieden
        """)
    parser.add_argument(
        'layers',
        type=str,
        help="""
        Name of the layers, for example
        stadsdeel,buurtcombinatie
        """)
    parser.add_argument(
        "srs",
        type=str,
        default="28992",
        choices=["28992", "4326"],
        help="choose srs (default: %(default)s)")
    return parser


def main():
    args = parser().parse_args()
    load_wfs_layers_into_postgres(
        args.config_path, args.db_config, args.url, args.layers, args.srs)


if __name__ == '__main__':
    main()
