from src.datapunt_processing.transform.geospatial import geocode_xls_to_csv
from types import ModuleType


def test_import_geocode_xls_to_csv():

    assert isinstance(geocode_xls_to_csv, ModuleType)
