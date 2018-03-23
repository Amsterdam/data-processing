from src.datapunt_processing.transform.geospatial import rd_to_wgs84
from types import ModuleType


def test_import_rd_to_wgs84():

    assert isinstance(rd_to_wgs84, ModuleType)
