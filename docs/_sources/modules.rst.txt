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

    extract/download_from_data_amsterdam_catalog
    extract/download_from_data_amsterdam_api
    extract/download_from_objectstore
    extract/download_from_wfs
    
Transform Geospatial
--------------------

**Functions to spatial transform and enrich datasets.**

.. toctree::
    :maxdepth: 1

    transform/geospatial/postgres_add_areas_from_coordinates
    transform/geospatial/api_clean_BAG_address_NED
    transform/geospatial/api_get_nearest_address_from_latlon
    transform/geospatial/api_get_areacodes_from_latlon
    transform/geospatial/divide_bbox_amsterdam_in_quadrants
    transform/geospatial/rd_to_wgs84

Transform Enrichment
--------------------

**Functions to enrich datasets.**

.. toctree::
    :maxdepth: 1

    transform/enrichment/add_knmi_data

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

    _modules/helpers