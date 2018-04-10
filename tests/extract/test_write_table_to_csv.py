from src.datapunt_processing.extract import write_table_to_csv
from types import ModuleType


def test_import_write_table_to_csv():

    assert isinstance(write_table_to_csv, ModuleType)
