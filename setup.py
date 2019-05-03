#!/bin/python

from typing import NoReturn, List

from setuptools import find_packages, setup
from pathlib import Path


def requirements(reqs_path: Path = Path('requirements.txt')) -> List[str]:
    with open(reqs_path, 'r') as fhd:
        return fhd.readlines()


setup(
    name='songrecsys',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/pwr-projects/songsysrec',
    license='',
    author='Mateusz Gaweł, Grzegorz Suszk',
    # author_email='',
    description='',
    install_requires=requirements(),
)
