"""
    tests.download_from_wfs
    setup for testing, used this example:
    http://docs.python-guide.org/en/latest/writing/structure/
    ~~~~~~~~~~~~~~~~~~~~~
"""

from src.datapunt_processing.extract.download_from_wfs import get_layers_from_wfs, get_layer_from_wfs


def test_get_layers_from_wfs():
    url = "http://map.data.amsterdam.nl/maps/gebieden"
    testurl = get_layers_from_wfs(url)
    assert(isinstance(testurl,list))


def test_get_layer_from_wfs():
    url = "http://map.data.amsterdam.nl/maps/gebieden"
    layer_name = "stadsdeel"
    json = get_layer_from_wfs(url, layer_name, '4326','geojson')
    print(type(json))
    assert(isinstance(json, dict))
