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
    name='datapunt_amsterdam_processing',
    description="Data processing Functions",
    long_description=read('README.rst'),
    url='https://github.com/Amsterdam/data-processing',
    author='Amsterdam Datapunt',
    author_email='datapunt@amsterdam.nl',
    license='Mozilla Public License Version 2.0',
    classifiers=[
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],


    # Entry points:
    entry_points={
        'console_scripts': [
            'extract = extract.main:main',
            'transform = transform.main:main',
            'load = load.main:main'
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
        'docutils',
        'jsonschema',
        'mimeparse',
        'PyYaml',
        'PyJWT',
        'SQLAlchemy==1.1',
        'swagger-parser',
    ],
    extras_require={
        'docs': [
            'MacFSEvents',
            'Sphinx',
            'sphinx-autobuild',
            'sphinx-autodoc-typehints',
            'sphinx_rtd_theme',
        ],
        'test': [
            'pytest',
            'pytest-cov',
        ],
        'dev': [
            'jupyter',
        ]
    },
)
