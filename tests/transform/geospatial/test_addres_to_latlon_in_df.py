from src.datapunt_processing.transform.geospatial import addres_to_latlon_in_df
from types import ModuleType


def test_import_addres_to_latlon_in_df():

    assert isinstance(addres_to_latlon_in_df, ModuleType)
