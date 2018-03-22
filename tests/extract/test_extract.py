from src.extract.download_from_data_amsterdam_catalog import download_all_files, download_metadata


def test_download_from_data_amsterdam_catalog():
    url ='https://data.amsterdam.nl/#?dte=catalogus%2Fapi%2F3%2Faction%2Fpackage_show%3Fid%3D42e270c2-c19d-45c7-a8c7-061633b6bc38&dtfs=T&dsf=groups::verkeer-infrastructuur&mpb=topografie&mpz=11&mpv=52.3731081:4.8932945'
    metadata = download_metadata(url)
    download_all_files(metadata, 'data')
    #assert('data)

