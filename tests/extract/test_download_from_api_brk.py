from src.datapunt_processing.extract import download_from_api_brk
from types import ModuleType


def test_import_download_from_api_brk():

    assert isinstance(download_from_api_brk, ModuleType)
