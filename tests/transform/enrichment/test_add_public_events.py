from src.datapunt_processing.transform.enrichment import add_public_events
from types import ModuleType


def test_import_add_public_events():

    assert isinstance(add_public_events, ModuleType)
