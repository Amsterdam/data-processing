#!/usr/bin/env python
"""See <https://setuptools.readthedocs.io/en/latest/>.
"""
import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    # Publication Metadata:
    version='0.0.1',
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


    # Entry points:
    entry_points={
        'console_scripts': [
            'download_from_data_amsterdam = extract.download_from_data_amsterdam:main',
            'csv_dataframe = extract.csv_dataframe:main',
            'load_wfs_to_postgres = load.load_wfs_to_postgres:main',
            'get_geojson_from_wfs = transform.geospatial.get_geojson_from_wfs:main',
            'load_xls_to_postgres = load.load_xls_to_postgres:main',
        ],
    },

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
        'python-swiftclient',
        'python-keystoneclient',

        # Config providers
        'datapunt-config-loader',
        'configparser==3.5.0',

        # db connectors
        'sqlalchemy==1.2.2',
        'psycopg2==2.7.3.2',

        # Transformers
        'pandas==0.22.0',

        # Utilities
        'docutils',
        'pprint>=0.1',
        'pyproj==1.9.5.1',
        'requests_cache==0.4.13',

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
        ],
        'dev': [
            'jupyter',
        ]
    },
    tests_require=[
            'pytest',
        ]
)
