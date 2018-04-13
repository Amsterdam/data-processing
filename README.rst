Data-processing
===============

.. image:: https://img.shields.io/badge/python-3.6-blue.svg
   :target: https://www.python.org/

.. image:: https://img.shields.io/badge/license-MPLv2.0-blue.svg
   :target: https://www.mozilla.org/en-US/MPL/2.0/

At the City of Amsterdam we deal with many different types of structured and unstructered data. Much of the data is not of high quality and are missing proper semantics to do proper analytics with.

This repository combines generic command line functions to create extract, transform and load steps we can then use for creating a reproducable data for analytics and usage in dashboards and maps.

For more information about the how we use these functions in our workflow, read the
`data-pipeline guide <https://amsterdam.github.io/guides/data-pipeline/>`_.

How to use
==========

Full documentation can be found here:
`amsterdam.github.io/data-processing <https://amsterdam.github.io/data-processing/>`_ 

Quickstart:
To use a function in python you can use::

    from datapunt_processing.extract import download_from_catalog

    or 

    from datapunt_processing.helpers.connections import objectstore_connection

To use the functions directly from the command line in your virtual environment or docker shell you can use it like this::
    
    download_from_data_amsterdam -h 

To see the list of command line functions see the modules below or directly in `setup.py <https://github.com/Amsterdam/data-processing/blob/master/setup.py#L60>`_


Getting Started
===============


To get the functions up and running:

.. code-block:: bash

    pip install datapunt-processing



To develop the functions locally use these steps:

1. Clone the repository:

.. code-block:: bash

    git clone https://github.com/Amsterdam/data-processing.git
    cd data-processing

2. Create Virtual environment in Windows

.. code-block:: bash

    # Create and activate a virtual environment, for example with:
    python -m venv --copies --prompt data-processing .venv 
    .venv\Scripts\activate

2. Create Virtual environment in OSX

.. code-block:: bash

    virtualenv --python=$(which python3) venv
    source venv/bin/activate 

3. Install the data-processing modules in editable mode

.. code-block:: bash    

    pip install -e .

4. A database is required for the transform and load functions. 
You can setup your postgres database credentials in the config.ini file to apply to the functions.

If want to use `Docker <https://www.docker.com>`_, you can start a database server for your project in a new terminal. The name, port and login of the database can be changed in the docker-compose.yml. Also change them in the config.ini file which will be used by the functions to connect to that database.


.. code-block:: bash    

    docker-compose up -d database

Notebooks
=========
Some of the examples are in the form of runnable Jupyter notebooks. Copies of these with all the images and output included are hosted at Anaconda Cloud. To run these notebooks on your own system, start up a Jupyter notebook server:

To install jupyter:

.. code-block:: bash

    pip install -e .\[dev\]

    jupyter notebook --NotebookApp.iopub_data_rate_limit=100000000

How to Contribute
=================
If you want to contribute please follow the `contribute guidelines <https://amsterdam.github.io/CONTRIBUTING/>`_ 

0. Prequisites
--------------
Fork this repository to your local github account to add add and test new functions.

.. code-block:: bash

    git clone https://github.com/Amsterdam/data-processing.git

Install the docs,test,dev packages using this command:

.. code-block:: bash

    pip install -e .[docs,test,dev]
    or when using zsh
    pip install -e .\[docs,test,dev\]

This package is build by using `setuptools <http://setuptools.readthedocs.io>`_ to be able to release stable versions on PyPi. It follows some of `these <http://alexanderwaldin.github.io/packaging-python-project.html>`_ guidelines of setting up a python package.

1. Add function
---------------
We try to use command line functions as much as possible to ensure we create functions to work easily with different environments and to force yourself creating more generic functions with input variables.

If possible, convert your function into a `python-package command line script <https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html>`_ using the `boilerplate_function.py <https://github.com/Amsterdam/data-processing/blob/master/src/boilerplate_function.py>`_ 

Add your function to the appropriate `folder <https://github.com/Amsterdam/data-processing/tree/master/src/datapunt_processing>`_:
    - `extract <https://github.com/Amsterdam/data-processing/tree/master/src/datapunt_processing/extract>`_
    - `transform <https://github.com/Amsterdam/data-processing/tree/master/src/datapunt_processing/transform>`_
    - `load <https://github.com/Amsterdam/data-processing/tree/master/src/datapunt_processing/load>`_
    - `helpers  <https://github.com/Amsterdam/data-processing/tree/master/src/datapunt_processing/helpers>`_


side note: not all functions are suitable for CL. Machine learning preprocessing steps or general API calls for instance, (that often require parameters in the form of dicts or lists) as input are not suitable and can be used as stand-alone scripts. 

2. Add tests
------------

Add test to the `test folder <https://github.com/Amsterdam/data-processing/tree/master/tests>`_ and run:

.. code-block:: bash

    python setup.py test

to test if no other functions are breaking. Correct those issues as well if needed.

3. Add documentation
--------------------
Create a awesome_module.rst file with `Sphinx Argparse extension <http://sphinx-argparse.readthedocs.io/en/latest/>`_ fields to generate the description and argument fields by reusing an `existing rst file <https://github.com/Amsterdam/data-processing/blob/master/sphinx/source/extract/download_from_data_amsterdam.rst>`_. The helpers docs will generate automatically, so you can skip this step if it is placed in the helper function. 

Add the rst filename to the list in `modules.rst <https://github.com/Amsterdam/data-processing/blob/master/sphinx/source/modules.rst>`_ to be found on the main page.

Regenerate the documentation to test the docs output using this command line function:

.. code-block:: bash

    sphinx/make docs
    and test if the readme is not broken:
    open docs/index.html

4. Add a Pull Request
---------------------
Make a PR to add the add your awesome function to our processing code to be reused by many other developpers and data analists.

