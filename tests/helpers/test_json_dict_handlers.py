from src.datapunt_processing.helpers import json_dict_handlers
from types import ModuleType


def test_import_json_dict_handlers():

    assert isinstance(json_dict_handlers, ModuleType)
