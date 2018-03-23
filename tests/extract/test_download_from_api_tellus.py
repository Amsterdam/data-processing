from src.datapunt_processing.extract import download_from_api_tellus
from types import ModuleType


def test_import_download_from_api_tellus():

    assert isinstance(download_from_api_tellus, ModuleType)
