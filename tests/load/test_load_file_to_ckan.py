#!/usr/bin/env python3
from src.datapunt_processing.load import load_file_to_ckan
from types import ModuleType


def test_import_load_file_to_ckan():
    assert isinstance(load_file_to_ckan, ModuleType)
