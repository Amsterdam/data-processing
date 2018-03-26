from src.datapunt_processing.helpers import logging
from types import ModuleType


def test_import_xml_logging():

    assert isinstance(logging, ModuleType)
