#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  16 13:45:04 2020
@author: Ahmed Qamesh
"""

from setuptools import setup, find_packages



setup(
    name="school_statistics_study",
    version="0.1.0",
    author="Ahmed Qamesh",
    author_email="ahmed.qamesh@cern.ch",
    description="A school statistics study",
    packages=find_packages(),
    install_requires=['coloredlogs', 'verboselogs', 'aenum'],    
    include_package_data=True,
    entry_points={
        "console_scripts": ["run_study = main_lib.school_study:main"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)