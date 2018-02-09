import os
import pytest
from extract import download_from_data_amsterdam


def test_location_config_file():
    import configparser
    from extract.download_from_objectstore import readConfig
    test = readConfig('config.ini')
    assert isinstance(test, configparser.RawConfigParser)
    print(test)

def test_load_data_amsterdam():
    url ='https://data.amsterdam.nl/#?dte=catalogus%2Fapi%2F3%2Faction%2Fpackage_show%3Fid%3D42e270c2-c19d-45c7-a8c7-061633b6bc38&dtfs=T&dsf=groups::verkeer-infrastructuur&mpb=topografie&mpz=11&mpv=52.3731081:4.8932945'
    meta_id = '42e270c2-c19d-45c7-a8c7-061633b6bc38'
    download_from_data_amsterdam meta_id test