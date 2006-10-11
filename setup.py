#!/usr/bin/env python
"""Distutils setup file"""

import ez_setup
ez_setup.use_setuptools()
from setuptools import setup

# Metadata
PACKAGE_NAME = "simplegeneric"
PACKAGE_VERSION = "0.6"

def get_description():
    # Get our long description from the documentation
    f = file('README.txt')
    lines = []
    for line in f:
        if not line.strip():
            break     # skip to first blank line
    for line in f:
        if line.startswith('.. contents::'):
            break     # read to table of contents
        lines.append(line)
    f.close()
    return ''.join(lines)

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    description= "Simple generic functions (similar to Python's own len(), "
        "pickle.dump(), etc.)",
    long_description = get_description(),
    url = "http://cheeseshop.python.org/pypi/simplegeneric",
    author="Phillip J. Eby",
    author_email="peak@eby-sarna.com",
    license="PSF or ZPL",
    test_suite = 'simplegeneric.test_suite',
    py_modules = ['simplegeneric'],
)

