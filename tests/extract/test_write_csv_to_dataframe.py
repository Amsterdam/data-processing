from src.datapunt_processing.extract import write_csv_to_dataframe
from types import ModuleType


def test_import_write_csv_to_dataframe():

    assert isinstance(write_csv_to_dataframe, ModuleType)
