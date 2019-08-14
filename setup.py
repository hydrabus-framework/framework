#!/usr/bin/env python

import atexit
import errno
import os
import re
import subprocess
import tarfile
import traceback

from setuptools import setup, find_packages
from setuptools.command.install import install


__author__ = "Ghecko <ghecko78@gmail.com>"

description = 'Hydrabus Framework core'
name = 'hydrabus_framework'


def _extract_tarball(filename):
    tar = tarfile.open(filename)
    path = re.sub(r'\.tar.gz$', '', filename)
    setup_dir = '{}/{}'.format(path, tar.getmembers()[0].name)
    tar.extractall(path)
    tar.close()
    return setup_dir


def _get_modules(requests, github_base_url):
    modules = []
    resp = requests.request('GET', '{}{}'.format(github_base_url, '/orgs/hydrabus-framework/repos'))
    if resp.status_code == 200:
        for pkg in resp.json():
            modules.append(pkg["name"])
    return modules


def _get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


def _get_latest_release(requests, github_base_url, module):
    """
    Get the latest release of a module, if no release
    :param module: module name
    :return: url or None if not found
    """
    module_release_url = github_base_url + '/repos/hydrabus-framework/{}/releases/latest'.format(module)
    resp = requests.request('GET', module_release_url)
    if resp.status_code == 200:
        return resp.json()["tarball_url"]
    else:
        return None


def _download_release(requests, module_tarball_url):
    resp = requests.request('GET', module_tarball_url)
    if resp.status_code == 200:
        filename = '/tmp/hbfmodules/{}'.format(_get_filename_from_cd(resp.headers.get('content-disposition')))
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        open(filename, 'wb').write(resp.content)
        return filename
    return None


def _post_install():
    print('----------------------------------------------------------------------')
    print('------------------Get and install available modules-------------------')
    print('----------------------------------------------------------------------')
    github_base_url = 'https://api.github.com'
    requests = __import__('requests')
    installed = 0
    not_installed = []
    modules = _get_modules(requests, github_base_url)
    if len(modules) > 0:
        for module in modules:
            release_tarball_url = _get_latest_release(requests, github_base_url, module)
            if release_tarball_url:
                filename = _download_release(requests, release_tarball_url)
                if filename:
                    setup_dir = _extract_tarball(filename)
                    try:
                        return_code = subprocess.call(['python', 'setup.py', 'install'], cwd=setup_dir)
                        if return_code != 0:
                            not_installed.append(module)
                        else:
                            installed += 1
                    except:
                        print("Unable to install {} module".format(module))
                        traceback.print_exc()
                else:
                    print("Failed to download release for the module {}".format(module))
    print("{} module(s) installed".format(installed))
    if len(not_installed) > 0:
        print("These modules could not be installed: {}".format(not_installed))


class PostInstall(install):
    """
    This post install script download and install all available modules that have a released package
    """
    def __init__(self, *args, **kwargs):
        super(PostInstall, self).__init__(*args, **kwargs)
        atexit.register(_post_install)


setup(
    name=name,
    version='0.1.0',
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
    scripts=['hydrabus_framework/hbfconsole'],
    cmdclass={
        'install': PostInstall,
    },
)
