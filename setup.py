#!/bin/python

from typing import NoReturn, Text

from setuptools import find_packages, setup


def requirements(reqs_path: Text = "requirements.txt") -> NoReturn:
    with open(reqs_path, "r") as fhd:
        return fhd.readlines()


setup(
    name="songrecsys",
    version="0.1",
    packages=find_packages(),
    url="https://github.com/pwr-projects/songsysrec",
    license="",
    author="Mateusz Gaweł, Grzegorz Suszka",
    # author_email='',
    description="",
    install_requires=requirements(),
)
