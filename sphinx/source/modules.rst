.. _modules:

Data Processing modules
=======================

Data Processing contains 4 main modules: Auth, Extract, Transform and Load (the standard ETL processing) and one Helper function module to re-use often used generic functions.

Auth
----

**Fill in the config.ini.example with the proper user credentials for the
project.
Rename this file to config.ini. 
Do not store passwords in this file
Use .gitignore to ignore .ini files to prevent uploading
them to github.**


Extract
-------

**Functions to extract data from the Objectstore where raw files are
stored, from API’s or from the data catalog**

.. toctree::
    :maxdepth: 1

    extract/download_from_data_amsterdam

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

    load/load_wfs_into_postgres

Helper functions
----------------

**Generic functions for most commonly used data operations**

.. toctree::
    :maxdepth: 1

    helper_functions