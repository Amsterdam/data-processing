#!/usr/bin/env python3
from src.datapunt_processing.load import load_xls_to_postgres
from types import ModuleType


def test_import_load_xls_to_postgres():
    assert isinstance(load_xls_to_postgres, ModuleType)
