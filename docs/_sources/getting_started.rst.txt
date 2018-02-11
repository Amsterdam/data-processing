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
    or when using zsh
    pip install -e ./[docs,test,dev/]

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
