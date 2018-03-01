"""
    tests.test_geospatial
    setup for testing, used this example:
    http://docs.python-guide.org/en/latest/writing/structure/
    ~~~~~~~~~~~~~~~~~~~~~
"""

from src.transform.geospatial.get_geojson_from_wfs import get_layers_from_wfs, get_geojson_from_wfs


def test_get_layers_from_wfs():
    url = "http://map.data.amsterdam.nl/maps/gebieden"
    testurl = get_layers_from_wfs(url)
    assert(isinstance(testurl,list))


def test_get_geojson_from_wfs():
    url = "http://map.data.amsterdam.nl/maps/gebieden"
    layer_name = "stadsdeel"
    json = get_geojson_from_wfs(url, layer_name, '4326')
    print(type(json))
    assert(isinstance(json, dict))
