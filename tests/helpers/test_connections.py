from src.datapunt_processing.helpers import connections
from types import ModuleType


def test_import_connections():

    assert isinstance(connections, ModuleType)
