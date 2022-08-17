#!/usr/bin/env python
from setuptools import setup

setup(
    name="appgallery-connect",
    version="0.0.1",
    description="DPMN tap for extracting data",
    author="",
    url="",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["appgallery_connect"],
    install_requires=[
        # NB: Pin these to a more specific version for tap reliability
        "requests",
    ],
    entry_points="""
    [console_scripts]
    appgallery-connect=appgallery_connect:main
    """,
    packages=["appgallery_connect"],
    package_data={
        "appgallery_connect/schemas": [
            "installations_by_date.json"
        ]
    },
    include_package_data=True,
)
