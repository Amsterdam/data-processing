from src.datapunt_processing.transform.geospatial import api_clean_BAG_address_NED
from types import ModuleType


def test_import_api_clean_BAG_address_NED():

    assert isinstance(api_clean_BAG_address_NED, ModuleType)
