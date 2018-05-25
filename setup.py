#!/usr/bin/env python
"""
See <https://setuptools.readthedocs.io/en/latest/>.
best practices: https://docs.pytest.org/en/latest/goodpractices.html
For Pypi deployment steps: https://packaging.python.org/tutorials/distributing-packages/
"""
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    """ Custom class to avoid depending on pytest-runner.
    """
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['--cov', find_packages('src')]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    # Publication Metadata:
    version='0.0.1a10',
    name='datapunt_processing',
    description="Datapunt generic ETL command line scripts and functions for shell scripting in Docker.",
    long_description=read('README.rst'),
    url='https://github.com/Amsterdam/data-processing',
    author='Amsterdam Datapunt',
    author_email='datapunt@amsterdam.nl',
    license='Mozilla Public License Version 2.0',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],


    # Entry points - pls try to keep some order when adding functions, placing it in adequate section: load/transform etc..
    entry_points={
        'console_scripts': [
            # extract
            'download_from_catalog = datapunt_processing.extract.download_from_catalog:main',
            'download_from_api_with_authentication = datapunt_processing.extract.download_from_api_with_authentication:main',
            'download_from_api_brk = datapunt_processing.extract.download_from_api_brk:main',
            'download_from_api_tellus = datapunt_processing.extract.download_from_api_tellus:main',
            'download_from_api_kvk = datapunt_processing.extract.download_from_api_kvk:main',
            'download_from_wfs = datapunt_processing.extract.download_from_wfs:main',
            'download_from_objectstore = datapunt_processing.extract.download_from_objectstore:main',
            'download_from_ckan = datapunt_processing.extract.download_from_ckan:main',
            'write_csv_to_dataframe = datapunt_processing.extract.csv_dataframe:main',
            'write_table_to_csv = datapunt_processing.extract.write_table_to_csv:main',
            'write_table_to_geojson = datapunt_processing.extract.write_table_to_geojson:main',
            'write_mdb_to_csv = datapunt_processing.extract.write_mdb_to_csv:main',
            # load
            'load_wfs_to_postgres = datapunt_processing.load.load_wfs_to_postgres:main',
            'load_xls_to_postgres = datapunt_processing.load.load_xls_to_postgres:main',
            'load_file_to_ckan = datapunt_processing.load.load_file_to_ckan:main',
            'load_file_to_objectstore = datapunt_processing.load.load_file_to_objectstore:main',
            #transform
            'api_clean_BAG_address_NED = datapunt_processing.transform.geospatial.api_clean_BAG_address_NED:main',
            'get_geojson_from_wfs = datapunt_processing.transform.geospatial.get_geojson_from_wfs:main',
            'geocode_xls_to_csv = datapunt_processing.transform.geospatial.geocode_xls_to_csv:main',
            'postgres_add_areas_from_coordinates = datapunt_processing.transform.geospatial.postgres_add_areas_from_coordinates:main',
            'add_public_events = datapunt_processing.transform.enrichment.add_public_events:main',
            'add_knmi_data = datapunt_processing.transform.enrichment.add_knmi_data:main',
            #data visualization
            'heatmap = datapunt_processing.data_visualization.heatmap:main'
        ],
    },
    # Add custom pytester class
    cmdclass={'test': PyTest},
    # Packages and Package Data:
    package_dir={'': 'src'},
    packages=find_packages('src'),
    package_data={
        # Not yet needed 'extract': ['config_schema*.json', 'openapi*.json', 'openapi.yml']
    },
    # Requirements:
    install_requires=[

        # Getters
        'requests==2.18.4',
        'xlrd==1.1.0',
        'lxml==4.2.1',
        'python-swiftclient==3.4.0',
        'python-keystoneclient',

        # Config providers
        'datapunt-config-loader',
        'configparser==3.5.0',

        # db connectors
        'sqlalchemy==1.2.2',
        'psycopg2==2.7.3.2',
        #'pygdal>=1.8.1.0',

        # Transformers
        'pandas==0.22.0',
        'scikit-learn==0.19.1',
        # Utilities
        'docutils',
        'pprint>=0.1',
        'requests_cache==0.4.13',
        'logger==1.4',
        'ipython==5.5.0',
        # Data visualization
        'pillow==5.1.0'

    ],
    extras_require={
        'docs': [
            #'MacFSEvents',
            'Sphinx',
            'sphinx-autobuild',
            #'sphinx-autodoc-typehints',
            'sphinx-argparse',
            'sphinx_rtd_theme',
        ],
        'test': [
            'pytest',
            'pytest-runner',
            'pytest-cov',
            'flake8'
        ],
        'dev': [
            'jupyter',
        ]
    }
)
