#!/usr/bin/env python
from setuptools import find_packages, setup
import os
import re


ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = \'([0-9.]+)\'''')


def get_version():
    init = open(os.path.join(ROOT, 'groceries', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


setup(
    name='groceries-cli',
    version=get_version(),
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click==5.1',
        'coverage==3.7.1',
        'coveralls==0.5',
        'flake8==2.4.1',
        'mock==1.3.0',
        'pytest==2.7.2',
        'pyyaml==3.11',
        'requests==2.7.0',
        'tox==2.1.1',
    ],
    entry_points='''
        [console_scripts]
        groceries=groceries.core:cli
    ''',
)
