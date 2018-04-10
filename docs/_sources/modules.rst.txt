.. _modules:

Modules
=======

Data Processing contains 4 main modules:

    1. Extract
    2. Transform
    3. Load 
    4. Helpers


Basic usage
-----------

**Fill in the config.ini with the proper testuser credentials for the
project. 
Do not store passwords in this file but use ENV variables with `export ENV=****`
Use .gitignore to ignore .ini files to prevent uploading
them to github.**

Extract
-------

**Functions to extract data from the Objectstore where raw files are
stored, from API’s or from the data catalog.**

.. toctree::
    :maxdepth: 1

    extract/download_from_catalog
    extract/download_from_objectstore
    extract/download_from_wfs
    extract/download_from_api_with_authentication
    extract/download_from_api_brk
    extract/download_from_api_tellus
    extract/download_from_api_kvk
    extract/write_table_to_csv
    extract/write_mdb_to_csv
    extract/write_csv_to_dataframe
    
Transform Geospatial
--------------------

**Functions to spatial transform and enrich datasets.**

.. toctree::
    :maxdepth: 1

    transform/geospatial/postgres_add_areas_from_coordinates
    transform/geospatial/api_clean_BAG_address_NED
    transform/geospatial/api_get_nearest_address_from_coordinate
    transform/geospatial/api_get_area_codes_from_latlon
    transform/geospatial/divide_bbox_amsterdam_in_quadrants
    transform/geospatial/rd_to_wgs84
    
Transform Enrichment
--------------------

**Functions to enrich datasets.**

.. toctree::
    :maxdepth: 1

    transform/enrichment/add_knmi_data
    transform/enrichment/add_public_events

Load
----
**Common functions to load data into the Objectstore, CKAN (our public data.amsterdam.nl) or PostgreSQL.**


.. toctree::
    :maxdepth: 1

    load/load_file_to_objectstore
    load/load_file_to_ckan
    load/load_xls_into_postgres
    load/load_wfs_into_postgres

Helpers
-------

**Generic helper functions for most commonly used data operations.**

.. toctree::
    :maxdepth: 1

    _modules/datapunt_processing.helpers