from src.datapunt_processing.extract import download_from_catalog
from types import ModuleType


def test_import_download_from_catalog():

    assert isinstance(download_from_catalog, ModuleType)
