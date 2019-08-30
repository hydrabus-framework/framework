#!/usr/bin/env python

from setuptools import setup, find_packages


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"

description = 'Hydrabus Framework core'
name = 'hydrabus_framework'


setup(
    name=name,
    version='0.0.1',
    packages=find_packages(),
    license='GPLv3',
    description=description,
    author='Ghecko',
    url='https://github.com/hydrabus-framework/framework',
    install_requires=[
        'tabulate==0.8.3',
        'prompt_toolkit==2.0.9',
        'serial==0.0.97',
        'pyserial==3.4',
        'requests==2.22.0'
    ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha'
    ],
    keywords=['hydrabus', 'framework', 'hardware', 'security', 'core', 'engine'],
    scripts=['hydrabus_framework/hbfconsole', 'hydrabus_framework/hbfupdate'],
    cmdclass={
        'install': PostInstall,
    },
)
