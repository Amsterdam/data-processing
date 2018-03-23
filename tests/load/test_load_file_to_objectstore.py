#!/usr/bin/env python3
from src.datapunt_processing.load import load_file_to_objectstore
from types import ModuleType


def test_import_load_file_to_objectstore():
    assert isinstance(load_file_to_objectstore, ModuleType)
