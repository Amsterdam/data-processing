#!/usr/bin/env python3
from src.load.load_wfs_to_postgres import run_command_sync


def test_run_command_sync():
    cmd =['ogr2ogr']
    test = run_command_sync(cmd)
    print(test)
    #assert(test, stderr)
