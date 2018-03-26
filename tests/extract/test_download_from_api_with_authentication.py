from src.datapunt_processing.extract import download_from_api_with_authentication
from types import ModuleType


def test_import_download_from_api_with_authentication():

    assert isinstance(download_from_api_with_authentication, ModuleType)
