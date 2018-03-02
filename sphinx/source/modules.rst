.. _modules:

Modules
=======

Data Processing contains 4 main modules: Auth, Extract, Transform and Load (the standard ETL processing) and one Helper function module to re-use often used generic functions.

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
stored, from API’s or from the data catalog**

.. toctree::
    :maxdepth: 1

    extract/download_from_data_amsterdam_catalog
    extract/download_from_data_amsterdam_api
    

Transform
---------

**Functions to transform, preprocess and enrich datasets. Divided into
the following subsections**

.. toctree::
    :maxdepth: 1

    transform/geospatial/get_geojson_from_wfs

Load
----
**Common functions to load data into PostgreSQL**


.. toctree::
    :maxdepth: 1

    load/load_xls_into_postgres
    load/load_wfs_into_postgres

Helpers
-------

**Generic helper functions for most commonly used data operations**

.. toctree::
    :maxdepth: 1

    _modules/helpers