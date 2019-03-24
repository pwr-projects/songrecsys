#!/bin/python

from setuptools import find_packages, setup

setup(
    name='songrecsys',
    version='0.0.0.0.0.0.0.0.1',
    packages=find_packages(),
    url='https://github.com/pwr-projects/songsysrec',
    license='',
    author='Mateusz Gaweł, Grzegorz Suszka',
    # author_email='',
    description='',
    install_requires=[
        'spotipy',
        'tqdm',
        'numpy'
    ]
)
