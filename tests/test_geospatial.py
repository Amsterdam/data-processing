"""
    tests.test_geospatial
    setup for testing, used this example:
    http://docs.python-guide.org/en/latest/writing/structure/
    ~~~~~~~~~~~~~~~~~~~~~
"""

import pytest
from context import get_geojson_from_wfs

# print(dir())

def test_get_layers_from_wfs():
    url = "http://map.data.amsterdam.nl/maps/gebieden"
    layer_name = "stadsdelen"
    testurl = get_geojson_from_wfs.get_layers_from_wfs(url)
    print(testurl)

test_get_layers_from_wfs()


def test_get_geojson_from_wfs():
    url = "http://map.data.amsterdam.nl/maps/gebieden"
    layer_name = "stadsdeel"
    json = get_geojson_from_wfs.get_geojson_from_wfs(url, layer_name)
    print(isinstance(json, str))

test_get_geojson_from_wfs()
