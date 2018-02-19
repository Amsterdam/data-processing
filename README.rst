Data-processing
===============

.. image:: https://img.shields.io/badge/python-3.6-blue.svg
   :target: https://www.python.org/

.. image:: https://img.shields.io/badge/license-MPLv2.0-blue.svg
   :target: https://www.mozilla.org/en-US/MPL/2.0/

Data preparation scripts for analysis projects using Python and Docker.
For more information about the complete workflow, read the
`data-pipeline guide <https://amsterdam.github.io/guides/data-pipeline/>`_.

This repo is a WIP so only the functions explained in the above docs are working. Please use a pull request to add new functions or code review. 

This package is build by using `setuptools <http://setuptools.readthedocs.io>`_ to be able to deploy this later on PyPi with version control. It follows some of `these <http://alexanderwaldin.github.io/packaging-python-project.html>`_ guidelines of setting up a python package.



Getting Started
===============

Clone the repository:

.. code-block:: bash

    git clone https://github.com/Amsterdam/data-processing.git
    cd data-processing

Create Virtual environment in Windows

.. code-block:: bash

    # Create and activate a virtual environment, for example with:
    python -m venv --copies --prompt data-processing .venv 
    .venv\Scripts\activate

Create Virtual environment in OSX

.. code-block:: bash

    virtualenv --python=$(which python3) venv
    source venv/bin/activate 

Install the data-processing modules in editable mode

.. code-block:: bash    

    pip install -e .[docs,test,dev]
    or when using zsh
    pip install -e ./[docs,test,dev/]

Start a database server in a new terminal (required for all load services with current config.ini or not using an existing database):

.. code-block:: bash    

    docker-compose up -d database


How to use
----------

The usage of the functions are described in full here:
`Data processing read the docs <https://amsterdam.github.io/data-processing/>`_ 

