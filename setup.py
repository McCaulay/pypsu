#!/usr/bin/env python
# pypsu - Python classes for working with PS2 PSU game save file formats.

import os
from setuptools import setup

PACKAGE_NAME = 'pypsu'
VERSION = '0.1.2'

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename), 'r').read()

setup(
    name=PACKAGE_NAME,
    description='Library for analyzing and creating PS2 PSU game save files',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license='MIT',
    version=VERSION,
    author='McCaulay Hudson',
    maintainer='McCaulay Hudson',
    author_email='mccaulayhudson@protonmail.com',
    url='https://github.com/McCaulay/pypsu',
    keywords='ps2 gamesave psu',
    platforms=['Unix', 'Windows'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    packages=[
        'psu',
    ],
    scripts=[
        'bin/psu'
    ],
    options={
        'bdist_wheel': {
            'universal': True
        }
    }
)