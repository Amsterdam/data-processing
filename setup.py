#!/usr/bin/env python
"""
See <https://setuptools.readthedocs.io/en/latest/>.
best practices: https://docs.pytest.org/en/latest/goodpractices.html
"""
import os, sys
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
    version='0.0.2',
    name='datapunt_processing',
    description="Data processing Functions",
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
            'download_from_data_amsterdam_catalog = extract.download_from_data_amsterdam_catalog:main',
            'download_from_tellus_api = extract.download_from_tellus_api:main',
            'download_from_objectstore = extract.download_from_objectstore:main',
            'csv_dataframe = extract.csv_dataframe:main',
            'download_from_kvk_api = extract.download_from_kvk_api:main',
            # load
            'load_wfs_to_postgres = load.load_wfs_to_postgres:main',
            'load_xls_to_postgres = load.load_xls_to_postgres:main',
            'load_file_to_ckan = load.load_file_to_ckan:main',
            'load_file_to_objectstore = load.load_file_to_objectstore:main',
            #transform
            'get_geojson_from_wfs = transform.geospatial.get_geojson_from_wfs:main',
            'postgres_add_areas_from_coordinates = transform.geospatial.postgres_add_areas_from_coordinates:main',
            'add_public_events = transform.enrichment.add_public_events:main',
            'add_knmi_data = transform.enrichment.add_knmi_data:main'
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

        # Utilities
        'docutils',
        'pprint>=0.1',
        'pyproj==1.9.5.1',
        'requests_cache==0.4.13',
        'logger==1.4',

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
