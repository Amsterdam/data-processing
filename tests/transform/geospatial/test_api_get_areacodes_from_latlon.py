from src.datapunt_processing.transform.geospatial import api_get_areacodes_from_latlon
from types import ModuleType


def test_import_api_get_areacodes_from_latlon():

    assert isinstance(api_get_areacodes_from_latlon, ModuleType)
