from src.datapunt_processing.extract import download_bbga_by_variable__area_year
from types import ModuleType


def test_import_download_bbga_by_variable__area_year():

    assert isinstance(download_bbga_by_variable__area_year, ModuleType)
