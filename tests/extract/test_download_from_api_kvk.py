from src.datapunt_processing.extract import download_from_api_kvk
from types import ModuleType


def test_import_download_from_api_kvk():

    assert isinstance(download_from_api_kvk, ModuleType)
