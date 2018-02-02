"""
    tests.test_geo_spatial
    ~~~~~~~~~~~~~~~~~~~~~
"""

import pytest
from transform.geospatial import get_geojson_from_wfs


def test_get_layers_from_wfs():
    url = "http://map.data.amsterdam.nl/maps/gebieden"
    layer_name = "stadsdelen"
    get_layers_from_wfs(url)
