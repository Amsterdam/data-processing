from src.datapunt_processing.helpers import files
from types import ModuleType


def test_import_files():

    assert isinstance(files, ModuleType)
