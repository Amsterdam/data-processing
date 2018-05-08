from src.datapunt_processing.extract import write_table_to_geojson
from types import ModuleType


def test_import_write_table_to_geojson():

    assert isinstance(write_table_to_geojson, ModuleType)
