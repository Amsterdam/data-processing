#!/usr/bin/env python3
import requests
import argparse
from datetime import datetime
import xml.etree.ElementTree as ET
from helpers.files import save_file
from helpers.logging import logger

logging = logger()


def get_layers_from_wfs(url_wfs):
    """
        Get all layer names in WFS service, print and return them in a list.
    """
    layer_names = []
    parameters = {"REQUEST": "GetCapabilities",
                  "SERVICE": "WFS"
                  }
    getcapabilities = requests.get(url_wfs, params=parameters)
    # print(getcapabilities.text)
    root = ET.fromstring(getcapabilities.text)

    for neighbor in root.iter('{http://www.opengis.net/wfs/2.0}FeatureType'):
        # print(neighbor.tag, neighbor.attrib)
        logger.info("layername: " + neighbor[1].text)  # neighbor[0]==name, neighbor[1]==title
        layer_names.append(neighbor[1].text)
    return layer_names


def get_layer_from_wfs(url_wfs, layer_name, srs, outputformat):
    """
    Get layer from a wfs service.
    Args:
        1. url_wfs: full url of the WFS including https, excluding /?::

            https://map.data.amsterdam.nl/maps/gebieden

        2. layer_name: Title of the layer::

            stadsdeel

        3. srs: coordinate system number, excluding EPSG::

            28992

        4. outputformat: leave empty to return standard GML, else define json, geojson, txt, shapezip::

            geojson

    Returns:
        The layer in the specified output format.
    """
    parameters = {"REQUEST": "GetFeature",
                  "TYPENAME": layer_name,
                  "SERVICE": "WFS",
                  "VERSION": "2.0.0",
                  "SRSNAME": "EPSG:{}".format(srs),
                  "OUTPUTFORMAT": outputformat
                  }
    logger.info("Requesting data from {}, layer: {}".format(url_wfs, layer_name))
    response = requests.get(url_wfs, params=parameters)
    if outputformat in ('geojson, json'):
        geojson = response.json()
        logger.info("{} features returned.".format(str(len(geojson["features"]))))
        return geojson
    return response


def get_multiple_geojson_from_wfs(url_wfs, layer_names, srs, output_folder):
    """
    Get all layers and save them as a geojson

    Args:
        1. url_wfs: full url of the WFS including https, excluding /?::

            https://map.data.amsterdam.nl/maps/gebieden

        2. layer_names: single or multiple titles of the layers, separated by a comma without spaces::

            stadsdeel,buurtcombinatie,gebiedsgerichtwerken,buurt

        3. srs: coordinate system number, excluding EPSG::

            28992

        4. output_folder: define the folder to save the files::

            path_to_folder/another_folder

    """
    layer_names = layer_names.split(',')

    for layer_name in layer_names:
        filename = "{}_{}.geojson".format(layer_name, datetime.now().date())
        geojson = get_layer_from_wfs(url_wfs, layer_name, srs, 'geojson')
        save_file(geojson, output_folder, filename)


def parser():
    """Parser function to run arguments from the command line and to add description to sphinx."""
    parser = argparse.ArgumentParser(description="""
    Get multiple layers as a geojson file from a WFS service.
    command line example::

      download_from_wfs https://map.data.amsterdam.nl/maps/gebieden stadsdeel,buurtcombinatie output_folder

    """)
    parser.add_argument('url_wfs',
                        type=str,
                        help="WFS url, for example http://map.data.amsterdam.nl/maps/gebieden")
    parser.add_argument('layer_names',
                        type=str,
                        nargs="+",
                        help="Layers to export, separated by a , for example: stadsdeel,buurtcombinatie")
    parser.add_argument("srs",
                        type=str,
                        default="28992",
                        choices=["28992", "4326"],
                        help="choose srs (default: %(default)s)")
    parser.add_argument("output_folder",
                        type=str,
                        help="Set the output location path, for example output or projectdir/data")
    return parser


def main():
    args = parser().parse_args()
    print(args)
    get_layers_from_wfs(args.url_wfs)
    get_multiple_geojson_from_wfs(args.url_wfs,
                                  args.layer_names[0],
                                  args.srs,
                                  args.output_folder)


if __name__ == '__main__':
    main()
