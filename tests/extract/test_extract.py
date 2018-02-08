import os
import pytest
#from extract import download_from_objectstore


def test_location_config_file():
    import configparser
    from extract.download_from_objectstore import readConfig
    test = readConfig('config.ini')
    assert isinstance(test, configparser.RawConfigParser)
    print(test)

test_location_config_file()