#!/usr/bin/env python

from setuptools import setup, find_packages

__author__ = "Ghecko <ghecko78@gmail.com>"

description = 'Hydrabus Framework core'
name = 'hydrabus_framework'
setup(
    name=name,
    version='0.1.0',
    packages=find_packages(),
    license='GPLv3',
    description=description,
    author='Ghecko',
    url='https://github.com/hydrabus-framework/framework',
    install_requires=[
        'tabulate',
        'prompt_toolkit',
        'serial'
    ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha'
    ],
    keywords=['hydrabus', 'framework', 'hardware', 'security', 'core', 'engine'],
    scripts=['hydrabus_framework/hbfconsole']
)
