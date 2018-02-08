import requests
import xml.etree.ElementTree as ET


def get_layers_from_wfs(url_wfs):
    """Get all layer names in WFS service"""
    parameters = {"REQUEST": "GetCapabilities",
                  "SERVICE": "WFS"
                  }
    getcapabilities = requests.get(url_wfs, params=parameters)
    # print(getcapabilities.text)
    root = ET.fromstring(getcapabilities.text)
    for neighbor in root.iter('{http://www.opengis.net/wfs/2.0}FeatureType'):
        # print(neighbor.tag, neighbor.attrib)
        print("layername: " + neighbor[1].text)  # neighbor[0]==name, neighbor[1]==title


def get_geojson_from_wfs(url_wfs, layer_name):
    """Get all features from one layer in WFS service as a geojson"""
    parameters = {"REQUEST": "GetFeature",
                  "TYPENAME": layer_name,
                  "SERVICE": "WFS",
                  "VERSION": "2.0.0",
                  "OUTPUTFORMAT": "geojson"
                  }
    print("Requesting data from {}, layer: {}".format(url_wfs, layer_name))
    geojson = requests.get(url_wfs, params=parameters)
    geojson = geojson.json()
    print("{} features returned.".format(str(len(geojson["features"]))))

    return geojson

