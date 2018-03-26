#!/usr/bin/env python3
#from src.datapunt_processing.load.load_wfs_to_postgres import run_command_sync
from src.datapunt_processing.load import load_wfs_to_postgres
from types import ModuleType


def test_import_load_wfs_to_postgres():
    assert isinstance(load_wfs_to_postgres, ModuleType)

#def test_run_command_sync():
#    cmd =['ogr2ogr']
#    test = run_command_sync(cmd)
#    print(test)
    #assert(test, stderr)
