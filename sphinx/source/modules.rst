.. _modules:

Modules
=======

Data Processing contains 5 modules: 
1. Authentication
2. Extract
3. Transform
4. Load 
5. Helpers


Authentication
--------------

**Fill in the config.ini.example with the proper user credentials for the
project.
Rename this file to config.ini. 
Do not store passwords in this file
Use .gitignore to ignore .ini files to prevent uploading
them to github.**

.. toctree::
    :maxdepth: 1

    _modules/authentication

Extract
-------

**Functions to extract data from the Objectstore where raw files are
stored, from API’s or from the data catalog.**

.. toctree::
    :maxdepth: 1

    datapunt_processing/extract/download_from_catalog
    datapunt_processing/extract/download_from_objectstore
    datapunt_processing/extract/download_from_wfs
    datapunt_processing/extract/download_from_api_with_authentication
    datapunt_processing/extract/download_from_api_brk
    datapunt_processing/extract/download_from_api_tellus
    datapunt_processing/extract/download_from_api_kvk
    
    
Transform Geospatial
--------------------

**Functions to spatial transform and enrich datasets.**

.. toctree::
    :maxdepth: 1

    datapunt_processing/transform/geospatial/postgres_add_areas_from_coordinates
    datapunt_processing/transform/geospatial/api_clean_BAG_address_NED
    datapunt_processing/transform/geospatial/api_get_nearest_address_from_latlon
    datapunt_processing/transform/geospatial/api_get_areacodes_from_latlon
    datapunt_processing/transform/geospatial/divide_bbox_amsterdam_in_quadrants
    datapunt_processing/transform/geospatial/rd_to_wgs84

Transform Enrichment
--------------------

**Functions to enrich datasets.**

.. toctree::
    :maxdepth: 1

    datapunt_processing/transform/enrichment/add_knmi_data

Load
----
**Common functions to load data into the Objectstore, CKAN (our public data.amsterdam.nl) or PostgreSQL.**


.. toctree::
    :maxdepth: 1

    datapunt_processing/load/load_file_to_objectstore
    datapunt_processing/load/load_file_to_ckan
    datapunt_processing/load/load_xls_into_postgres
    datapunt_processing/load/load_wfs_into_postgres

Helpers
-------

**Generic helper functions for most commonly used data operations.**

.. toctree::
    :maxdepth: 1

    _modules/helpers