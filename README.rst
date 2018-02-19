Data-processing
===============

.. image:: https://img.shields.io/badge/python-3.6-blue.svg
   :target: https://www.python.org/

.. image:: https://img.shields.io/badge/license-MPLv2.0-blue.svg
   :target: https://www.mozilla.org/en-US/MPL/2.0/

Data preparation scripts for analysis projects using Python and Docker.

This repo is a WIP so only the functions explained in the above docs are working. Please use a pull request to add new functions or code review. 

This package is build by using `setuptools <http://setuptools.readthedocs.io>`_ to be able to deploy this later on PyPi with version control. It follows some of `these <http://alexanderwaldin.github.io/packaging-python-project.html>`_ guidelines of setting up a python package.

How to use
==========

The usage of the functions are described here:
`amsterdam.github.io/data-processing <https://amsterdam.github.io/data-processing/>`_ 


Getting Started
===============

To get the functions up and running, also for running them from the command line, follow these 4 steps:

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

4. Start a database server in a new terminal (required for all load services with current config.ini or not using an existing database):

.. code-block:: bash    

    docker-compose up -d database


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
    pip install -e ./[docs,test,dev/]

Steps to add code
-----------------

1. Convert your function into a commandline script using the `boilerplate_function.py <https://github.com/Amsterdam/data-processing/blob/master/src/boilerplate_function.py>`_ 
   
   See the explanation here: `python-packaging - command line scripts <https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html>`_

2. Add your commandline name and location to the `concole_scripts <https://github.com/Amsterdam/data-processing/blob/master/setup.py#L36>`_ in setup.py

3. Add a rst file to generate the description and argument fields by reusing an `existing rst file <https://github.com/Amsterdam/data-processing/blob/master/sphinx/source/extract/download_from_data_amsterdam.rst>`_. Helpers will generate automatically, so you can skip this step if it is only a helper function.
It uses the `Sphinx Argparse extension <http://sphinx-argparse.readthedocs.io/en/latest/>`_ to generate the documentation, but to get this to work it needs a rst file.

4. Regenerate the documentation using:

.. code-block:: bash
    
    sphinx/make docs


Workflow
========

For more information about the complete workflow, read the
`data-pipeline guide <https://amsterdam.github.io/guides/data-pipeline/>`_.

