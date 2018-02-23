#!/usr/bin/env python3
import os
import requests
import argparse
from datetime import datetime
import xml.etree.ElementTree as ET
from helpers.files import save_file


def parser():
    """Parser function to run arguments from the command line and to add description to sphinx."""
    parser = argparse.ArgumentParser(description="""
Get multiple layers as a geojson file from a WFS service.
command line example: 
      `get_geojson_from_wfs https://map.data.amsterdam.nl/maps/gebieden stadsdeel,buurtcombinatie output_folder`
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
        print("layername: " + neighbor[1].text)  # neighbor[0]==name, neighbor[1]==title
        layer_names.append(neighbor[1].text)
    return layer_names


def get_geojson_from_wfs(url_wfs, layer_names, srs, output_folder):
    """
      Get all features from one layer in WFS service as a geojson.
    """
    layer_names = layer_names.split(',')
    # print(layer_names)
    for layer_name in layer_names:
        parameters = {"REQUEST": "GetFeature",
                      "TYPENAME": layer_name,
                      "SERVICE": "WFS",
                      "VERSION": "2.0.0",
                      "SRSNAME": "EPSG:{}".format(srs),
                      "OUTPUTFORMAT": "geojson"
                      }
        print("Requesting data from {}, layer: {}".format(url_wfs, layer_name))
        geojson = requests.get(url_wfs, params=parameters)
        geojson = geojson.json()
        print("{} features returned.".format(str(len(geojson["features"]))))

        suffix = '.geojson'
        filename = "{}_{}.geojson".format(layer_name, datetime.now().date())
        save_file(geojson, output_folder, filename)

    # return geojson


def main():
    args = parser().parse_args()
    print(args)
    get_layers_from_wfs(args.url_wfs)
    get_geojson_from_wfs(args.url_wfs, args.layer_names[0], args.srs, args.output_folder)


if __name__ == '__main__':
    main()
