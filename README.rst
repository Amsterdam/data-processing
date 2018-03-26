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

`amsterdam.github.io/data-processing <https://amsterdam.github.io/data-processing/>`_ 

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

Prequisites
-----------
Fork this repository to your local github account.

To add new documentation and test new functions, install the docs,test,dev packages using this command:

.. code-block:: bash    

    pip install -e .[docs,test,dev]
    or when using zsh
    pip install -e .\[docs,test,dev\]

Steps to add code
-----------------

This package is build by using `setuptools <http://setuptools.readthedocs.io>`_ to be able to deploy this later on PyPi with version control. It follows some of `these <http://alexanderwaldin.github.io/packaging-python-project.html>`_ guidelines of setting up a python package.

1. Convert your function into a `python-package command line script <https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html>`_ using the `boilerplate_function.py <https://github.com/Amsterdam/data-processing/blob/master/src/boilerplate_function.py>`_ 

side note: not all functions are suitable for CL. Machine learning preprocessing steps or general API calls for instance, (that often require parameters in the form of dicts or lists) as input are not suitable and can be used as stand-alone scripts. 

2. Add test to the `test folder <https://github.com/Amsterdam/data-processing/tree/master/tests>`_ and run 
.. code-block:: bash
    
    python setup.py test

to test if no other functions are breaking. Correct those issues if needed.

3. Add your commandline name and end point location to the `console_scripts <https://github.com/Amsterdam/data-processing/blob/master/setup.py#L36>`_ in setup.py.

4. Add a awesome_module.rst file with `Sphinx Argparse extension <http://sphinx-argparse.readthedocs.io/en/latest/>`_ fields to generate the description and argument fields by reusing an `existing rst file <https://github.com/Amsterdam/data-processing/blob/master/sphinx/source/extract/download_from_data_amsterdam.rst>`_. Helpers will generate automatically, so you can skip this step if it is only a helper function. 

5. add the rst file to the `modules.rst <https://github.com/Amsterdam/data-processing/blob/master/sphinx/source/modules.rst>`_ to be found on the main page.

6. Regenerate the documentation to test the docs output using:

.. code-block:: bash
    
    sphinx/make docs

6. Make a PR to add the add your awesome function to our processing code to be reused by many other developpers and data analists.


