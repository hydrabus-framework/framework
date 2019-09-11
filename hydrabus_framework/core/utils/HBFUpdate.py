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


class HBFUpdate:
    def __init__(self):
        self.github_base_url = 'https://api.github.com'
        self.logger = Logger()
        self.not_updated = []
        self.to_update = []
        self.to_install = []

    def _get_installed_modules(self):
        """
        Return a dict of currently installed module(s).
        :return: A dict of currently installed module(s) {'module_name': 'version', ...}
        """
        module_name = "hbfmodules"
        installed_modules = {}
        try:
            package = import_module(module_name)
        except ImportError:
            self.logger.handle('No modules currently installed', Logger.ERROR)
            return installed_modules
        for loader, module, is_pkg in pkgutil.walk_packages(package.__path__, prefix=package.__name__ + '.'):
            try:
                imported_module = import_module(module)
                for x in dir(imported_module):
                    obj = getattr(imported_module, x)
                    if inspect.isclass(obj) and issubclass(obj, AModule) and obj is not AModule:
                        installed_modules[module] = pkg_resources.get_distribution(module).version
            except ImportError:
                self.logger.handle('Error dynamically import package "{}"... Unable to update it'
                                   .format(module), Logger.ERROR)
                self.not_updated.append(module)
        return installed_modules

    def _get_available_modules(self):
        """
        Return a dict of module that have a release on the hydrabus-framework organization.
        :return: A dict of available module {'module_name': 'version', ...}
        """
        invalids = ['hbfmodules.skeleton', 'framework']
        modules = {}
        resp = requests.get('{}{}'.format(self.github_base_url, '/orgs/hydrabus-framework/repos'))
        if resp.status_code == 200:
            for pkg in resp.json():
                if pkg["name"] not in invalids:
                    module_release_url = self.github_base_url +\
                                         '/repos/hydrabus-framework/{}/releases/latest'.format(pkg["name"])
                    resp = requests.get(module_release_url)
                    if resp.status_code == 200:
                        modules[pkg["name"]] = resp.json()['tag_name']
        return modules

    def _get_latest_framework_version(self):
        """
        Return the latest release version of the Hydrabus framework
        :return: string
        """
        module_release_url = self.github_base_url + '/repos/hydrabus-framework/framework/releases/latest'
        resp = requests.get(module_release_url)
        if resp.status_code == 200:
            return resp.json()['tag_name']
        else:
            self.logger.handle('Unable to get the latest framework released version', Logger.ERROR)
            return None

    def _get_latest_release_url(self, module_name):
        """
        Get the latest release URL of a module or framework
        :param module_name: module name
        :return: url or None if not found
        """
        module_release_url = self.github_base_url + '/repos/hydrabus-framework/{}/releases/latest'.format(module_name)
        resp = requests.get(module_release_url)
        if resp.status_code == 200:
            return resp.json()["tarball_url"]
        else:
            self.logger.handle("Unable to retrieve latest release URL for module '{}'", Logger.ERROR)
            return None

    @staticmethod
    def _get_filename_from_cd(cd):
        """
        Get filename from content-disposition
        :param cd: Content-Disposition HTTP header
        :return: filename from Content-Disposition or None
        """
        if not cd:
            return None
        fname = re.findall('filename=(.+)', cd)
        if len(fname) == 0:
            return None
        return fname[0]

    def _download_release(self, module_tarball_url, package_name):
        """
        Download the latest release of a module or framework
        :param module_tarball_url: release URL
        :param package_name: The package name downloaded (module or framework)
        :return: filename or None
        """
        self.logger.handle("Downloading {}...".format(package_name))
        resp = requests.get(module_tarball_url, stream=True)
        if resp.status_code == 200:
            filename = '/tmp/hbfmodules/{}'.format(self._get_filename_from_cd(resp.headers.get('content-disposition')))
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
            open(filename, 'wb').write(resp.content)
            return filename
        return None

    @staticmethod
    def _extract_tarball(filename):
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

    def _manage_install(self, package_name):
        """
        Manage the installation of the specified package (module or framework)
        :param package_name: The package name to install (module or framework)
        :return: Bool: True if successfully update, False otherwise
        """
        release_tarball_url = self._get_latest_release_url(package_name)
        if release_tarball_url:
            filename = self._download_release(release_tarball_url, package_name)
            if filename:
                setup_dir = self._extract_tarball(filename)
                try:
                    return_code = subprocess.call(['python', 'setup.py', 'install'],
                                                  cwd=setup_dir, stdout=subprocess.DEVNULL)
                    if return_code != 0:
                        return False
                    else:
                        self.logger.handle("'{}' successfully installed".format(package_name), Logger.SUCCESS)
                        return True
                except:
                    self.logger.handle("The setup command are failed for the '{}' module".format(package_name), Logger.ERROR)
                    traceback.print_exc()
                    return False
            else:
                self.logger.handle("Failed to download the latest release for the module '{}'"
                                   .format(package_name), Logger.ERROR)
                return False
        else:
            return False

    def update(self, update_framework=None):
        """
        This script check all released Hydrabus Framework modules and compare it with currently installed modules.
        If an update is available, this script install it. Moreover, if a module is available and not installed, it will
        be installed
        :param update_framework: if True check if a framework update is available
        :return: Nothing
        """
        if update_framework:
            latest_release_version = self._get_latest_framework_version()
            if latest_release_version:
                if latest_release_version < pkg_resources.get_distribution('hydrabus_framework').version:
                    self.logger.handle('A new framework release is available, running update...', Logger.INFO)
                    if not self._manage_install('framework'):
                        self.not_updated.append('framework')
                else:
                    self.logger.handle('Hydrabus framework is up-to-date', Logger.SUCCESS)
            else:
                self.not_updated.append('framework')
        available_modules = self._get_available_modules()
        installed_modules = self._get_installed_modules()
        for module, version in available_modules.items():
            installed_module_version = installed_modules.get(module, None)
            if installed_module_version is not None:
                if installed_module_version < version:
                    self.to_update.append(module)
            else:
                self.to_install.append(module)
        for module_name in self.to_update:
            self.logger.handle("Update module '{}'".format(module_name), Logger.INFO)
            if not self._manage_install(module_name):
                self.not_updated.append(module_name)
        for module_name in self.to_install:
            self.logger.handle("Install module '{}'".format(module_name), Logger.INFO)
            if not self._manage_install(module_name):
                self.not_updated.append(module_name)
        if len(self.not_updated) > 0:
            self.logger.handle("Unable to update/install the following package:", Logger.ERROR)
            for module in self.not_updated:
                print(" - {}".format(module))
