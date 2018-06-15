from src.datapunt_processing.extract import write_xml_to_json
from types import ModuleType


def test_import_write_mdb_to_csv():

    assert isinstance(write_xml_to_json, ModuleType)
