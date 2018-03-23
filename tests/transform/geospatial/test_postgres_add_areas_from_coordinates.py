from src.datapunt_processing.transform.geospatial import postgres_add_areas_from_coordinates
from types import ModuleType


def test_import_postgres_add_areas_from_coordinates():

    assert isinstance(postgres_add_areas_from_coordinates, ModuleType)
