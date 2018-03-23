from src.datapunt_processing.transform.geospatial import divide_bbox_amsterdam_in_quadrants
from types import ModuleType


def test_import_divide_bbox_amsterdam_in_quadrants():

    assert isinstance(divide_bbox_amsterdam_in_quadrants, ModuleType)
