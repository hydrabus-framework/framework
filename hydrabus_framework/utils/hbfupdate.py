import errno
import inspect
import os
import pkg_resources
import pkgutil
import re
import requests
import subprocess
import tarfile
import traceback

from importlib import import_module

from hydrabus_framework.utils.logger import Logger
from hydrabus_framework.modules.AModule import AModule


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"

github_base_url = 'https://api.github.com'
logger = Logger()
not_updated = []
to_update = []
to_install = []


def get_installed_modules():
    """
    Return a dict of currently installed module(s).
    :return: A dict of currently installed module(s) {'module_name': 'version', ...}
    """
    module_name = "hbfmodules"
    installed_modules = {}
    try:
        package = import_module(module_name)
    except ImportError:
        logger.handle('No modules currently installed', Logger.ERROR)
        return installed_modules
    for loader, module, is_pkg in pkgutil.walk_packages(package.__path__, prefix=package.__name__ + '.'):
        try:
            imported_module = import_module(module)
            for x in dir(imported_module):
                obj = getattr(imported_module, x)
                if inspect.isclass(obj) and issubclass(obj, AModule) and obj is not AModule:
                    installed_modules[module] = pkg_resources.get_distribution(module).version
        except ImportError:
            logger.handle('Error dynamically import package "{}"... Unable to update it'.format(module), Logger.ERROR)
            not_updated.append(module)
    return installed_modules


def get_available_modules():
    """
    Return a dict of module that have a release on the hydrabus-framework organization.
    :return: A dict of available module {'module_name': 'version', ...}
    """
    invalids = ['hbfmodules.skeleton', 'framework']
    modules = {}
    resp = requests.get('{}{}'.format(github_base_url, '/orgs/hydrabus-framework/repos'))
    if resp.status_code == 200:
        for pkg in resp.json():
            if pkg["name"] not in invalids:
                module_release_url = github_base_url +\
                                     '/repos/hydrabus-framework/{}/releases/latest'.format(pkg["name"])
                resp = requests.get(module_release_url)
                if resp.status_code == 200:
                    modules[pkg["name"]] = resp.json()['tag_name']
    return modules


def get_latest_framework_version():
    """
    Return the latest release version of the Hydrabus framework
    :return: string
    """
    module_release_url = github_base_url + '/repos/hydrabus-framework/framework/releases/latest'
    resp = requests.get(module_release_url)
    if resp.status_code == 200:
        return resp.json()['tag_name']
    else:
        logger.handle('Unable to get the latest framework released version', Logger.ERROR)
        return None


def get_latest_release_url(module_name):
    """
    Get the latest release URL of a module or framework
    :param module_name: module name
    :return: url or None if not found
    """
    module_release_url = github_base_url + '/repos/hydrabus-framework/{}/releases/latest'.format(module_name)
    resp = requests.get(module_release_url)
    if resp.status_code == 200:
        return resp.json()["tarball_url"]
    else:
        logger.handle("Unable to retrieve latest release URL for module '{}'", Logger.ERROR)
        return None


def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]


def download_release(module_tarball_url, package_name):
    """
    Download the latest release of a module or framework
    :param module_tarball_url: release URL
    :param package_name: The package name downloaded (module or framework)
    :return:
    """
    logger.handle("Downloading {}...".format(package_name))
    resp = requests.get(module_tarball_url, stream=True)
    if resp.status_code == 200:
        filename = '/tmp/hbfmodules/{}'.format(get_filename_from_cd(resp.headers.get('content-disposition')))
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        open(filename, 'wb').write(resp.content)
        return filename
    return None


def extract_tarball(filename):
    """
    Extract the specified tarball
    :param filename: the tarball file path
    :return: Directory path of the extracted archive
    """
    tar = tarfile.open(filename)
    path = re.sub(r'\.tar.gz$', '', filename)
    setup_dir = '{}/{}'.format(path, tar.getmembers()[0].name)
    tar.extractall(path)
    tar.close()
    return setup_dir


def manage_install(package_name):
    """
    Manage the installation of the specified package (module or framework)
    :param package_name: The package name to install (module or framework)
    :return: Bool: True if successfully update, False otherwise
    """
    release_tarball_url = get_latest_release_url(package_name)
    if release_tarball_url:
        filename = download_release(release_tarball_url, package_name)
        if filename:
            setup_dir = extract_tarball(filename)
            try:
                return_code = subprocess.call(['python', 'setup.py', 'install'],
                                              cwd=setup_dir, stdout=subprocess.DEVNULL)
                if return_code != 0:
                    return False
                else:
                    logger.handle("'{}' successfully installed".format(package_name), Logger.SUCCESS)
                    return True
            except:
                logger.handle("The setup command are failed for the '{}' module".format(package_name), Logger.ERROR)
                traceback.print_exc()
                return False
        else:
            logger.handle("Failed to download the latest release for the module '{}'"
                          .format(package_name), Logger.ERROR)
            return False
    else:
        return False


def update(update_framework=None):
    """
    This script check all released Hydrabus Framework modules and compare it with currently installed modules.
    If an update is available, this script install it. Moreover, if a module is available and not installed, it will
    be installed
    :return: Nothing
    """
    if update_framework:
        latest_release_version = get_latest_framework_version()
        if latest_release_version:
            if latest_release_version < pkg_resources.get_distribution('hydrabus_framework').version:
                logger.handle('A new framework release is available, running update...', Logger.INFO)
                if not manage_install('framework'):
                    not_updated.append('framework')
            else:
                logger.handle('Hydrabus framework is up-to-date', Logger.SUCCESS)
        else:
            not_updated.append('framework')
    available_modules = get_available_modules()
    installed_modules = get_installed_modules()
    for module, version in available_modules.items():
        installed_module_version = installed_modules.get(module, None)
        if installed_module_version is not None:
            if installed_module_version < version:
                to_update.append(module)
        else:
            to_install.append(module)
    for module_name in to_update:
        logger.handle("Update module '{}'".format(module_name), Logger.INFO)
        if not manage_install(module_name):
            not_updated.append(module_name)
    for module_name in to_install:
        logger.handle("Install module '{}'".format(module_name), Logger.INFO)
        if not manage_install(module_name):
            not_updated.append(module_name)
    if len(not_updated) > 0:
        logger.handle("Unable to update/install the following package:", Logger.ERROR)
        for module in not_updated:
            print(" - {}".format(module))
