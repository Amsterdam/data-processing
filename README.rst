Data-processing
===============

.. image:: https://img.shields.io/badge/python-3.6-blue.svg
   :target: https://www.python.org/

.. image:: https://img.shields.io/badge/license-MPLv2.0-blue.svg
   :target: https://www.mozilla.org/en-US/MPL/2.0/

Data preparation scripts for analysis projects in python 3 and docker.
For more information about the complete workflow, read the
`data-pipeline
guide <https://amsterdam.github.io/guides/data-pipeline/>`.

This repo is a WIP so the scripts do not work properly yet.

This package is build by using `setuptools <http://setuptools.readthedocs.io>` to be able to deploy this later on PyPi with version control.

Getting Started
===============

.. code-block:: bash

    # Clone the repository:
    git clone git@github.com:Amsterdam/data-processing.git
    cd data-processing

    # Create and activate a virtual environment, for example with:
    python3.6 -m venv --copies --prompt data-processing .venv
    source ./.venv/bin/activate

    pip install -e .[docs,test,dev]

    # Start a database server (required for all sub-services):
    docker-compose up -d database

    # To test the service:
    (not ready yet)


Structure
---------

This repo uses 4 collections: auth, extract, transform and load. Each
collection contains specific scripts with an example and output file
which can be run using the the bash command, for example for
transformations: ``bash transform.sh``

Auth
~~~~

Fill in the config.ini.example with the proper user credentials for the
project and rename this file to config.ini. Do not store passwords in
this file and use .gitignore to ignore .ini files to prevent uploading
them to github.

-  Login to objectstore
-  Login to dev/docker databases
-  Access token to retrieve authenticated data from data.amsterdam.nl
   api’s.

Extract
~~~~~~~

**functions to extract data from the Objectstore where raw files are
stored, from API’s or from the data catalog**

::

        - csv_dataframe.py
        - download_bbga_by_variable__area_year.py
        - download_from_api.py
        - download_from_data_catalog.py
        - download_from_objectstore.py

Transform
~~~~~~~~~

**functions to transform, preprocess and enrich datasets. Divided into
the following subsections:**

-  data - common small datasets that can be used for the enrichment
   processes

   ::

         - amsterdam_hotspots.csv
         - centroid_streets.csv

-  data_visualization - common data visualization functions

   ::

         - .......

-  Enrichment - enrich files with other data sets

   ::

         -  add_public_events.py

-  geo_spatial - common geo functions

   ::

         - add_area_codes_from_centroid.py
         - clean_BAG_address_NED.py
         - divide_bbox_amsterdam_in_quadrants.py
         - get_centroid_street_NED.py
         - get_nearest_address-areacodes_from_latlon.py
         - rd_to_wgs84.py

-  helper_functions - templates for commonly used data operations

   ::

          - flatten_nested_json.py

-  preprocessing - common data preprocessing steps also for ML purposes

   ::

          - data_selection.py
          - ml_helperfunctions.py
          - ml_preprocessing.py

-  sql - common sql queries and operations

   ::

         - add_areacodes.sql
         - add_geom_column.sql

Load
~~~~

**Common functions to load data to the PostgreSQL dbs**

::

        - load_json_to_postgres.py
        - load_xls_to_postgres.py
