from src.datapunt_processing.helpers import xml_handlers
from types import ModuleType


def test_import_xml_handlers():

    assert isinstance(xml_handlers, ModuleType)
