#!/usr/bin/env python

import atexit
import importlib

from setuptools import setup, find_packages
from setuptools.command.install import install


__author__ = "Ghecko <ghecko78@gmail.com>"

description = 'Hydrabus Framework core'
name = 'hydrabus_framework'


def _post_install():
    print('----------------------------------------------------------------------')
    print('----------------Retrieve and install available modules----------------')
    print('----------------------------------------------------------------------')
    hbfupdate = importlib.import_module('hydrabus_framework.utils.hbfupdate')
    update = hbfupdate.update
    update()


class PostInstall(install):
    """
    This post install script download and install all available modules that have a released package
    """
    def __init__(self, *args, **kwargs):
        super(PostInstall, self).__init__(*args, **kwargs)
        atexit.register(_post_install)


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
