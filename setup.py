#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requirements = [
    'wheel>=0.23.0',
    'argparse>=1.2.1',
    'futures>=2.1.6',
    'six>=1.7.3',
    'psutil>=2.1.1',
    'nltk>=3.2.4',
    'networkx>=1.11'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='PositionRank',
    version='1.0',
    description='PositionRank: An Unsupervised Approach to Keyphrase Extraction from Scholarly Documents',
    author='Corina Florescu',
    author_email='corinaflorescu@my.unt.edu',
    packages=[
        'PositionRank',
    ],
    entry_points={'console_scripts': ['PositionRank = PositionRank.__main__:main']},
    package_dir={'PositionRank':
                 'PositionRank'},
    include_package_data=True,
    install_requires=requirements,
    license="GPLv3",
    zip_safe=False,
    keywords='deepwalk',
    classifiers=[

    ],
    test_suite='tests',
    tests_require=test_requirements
)
