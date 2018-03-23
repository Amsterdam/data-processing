from src.datapunt_processing.transform.geospatial import csv_get_centroid_of_street
from types import ModuleType


def test_import_csv_get_centroid_of_street():

    assert isinstance(csv_get_centroid_of_street, ModuleType)
