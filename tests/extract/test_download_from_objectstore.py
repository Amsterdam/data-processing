from src.datapunt_processing.extract import download_from_objectstore
from types import ModuleType


def test_import_download_from_objectstore():

    assert isinstance(download_from_objectstore, ModuleType)
