from src.datapunt_processing.transform.enrichment import add_knmi_data
from types import ModuleType


def test_import_add_knmi_data():

    assert isinstance(add_knmi_data, ModuleType)
