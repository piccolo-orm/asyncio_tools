#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

from asyncio_tools import __VERSION__ as VERSION


directory = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(directory, "README.md")) as f:
    LONG_DESCRIPTION = f.read()


setup(
    name="asyncio_tools",
    version=VERSION,
    description="Useful utilities for working with asyncio.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Daniel Townsend",
    author_email="dan@dantownsend.co.uk",
    python_requires=">=3.8.0",
    url="https://github.com/piccolo-orm/asyncio_tools",
    py_modules=["asyncio_tools"],
    data_files=[("", ["py.typed"])],
    install_requires=[],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
