from src.datapunt_processing.extract import download_from_ckan
from types import ModuleType


def test_import_download_from_ckan():

    assert isinstance(download_from_ckan, ModuleType)
