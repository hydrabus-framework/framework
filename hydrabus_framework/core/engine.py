import inspect
import pkgutil
import sys

from importlib import import_module
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.styles import Style

from hydrabus_framework.core.dispatcher import Dispatcher
from hydrabus_framework.modules.amodule import AModule
from hydrabus_framework.utils.logger import Logger


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


class HydraFramework:
    """
    Framework core engine
    """
    def __init__(self):
        self.logger = Logger()
        self.app_path = sys.path[0]
        self.current_module = None
        self.modules = self._list_modules()
        self.modules_history = []
        self.dispatcher = Dispatcher()
        self.prompt_style = Style.from_dict({
            # User input (default text).
            '': '#ffffff',

            # Prompt.
            'base': '#3399ff',
            'pound': '#3399ff',
            'module': '#ff0000 bold',
            'category': '#ffffff',
        })
        self.prompt = [
            ('class:base', '[hbf] '),
            ('class:module', ''),
            ('class:category', ''),
            ('class:pound', '> '),
        ]

    def update_prompt(self, module_name):
        """
        Update the user prompt
        :param module_name: The current module name
        """
        if module_name != "":
            category = module_name.split("/")[0]
            module = module_name.split("/")[1]
            self.prompt = [
                ('class:base', '[hbf] '),
                ('class:category', '{}'.format(category)),
                ('class:module', '({})'.format(module)),
                ('class:pound', '> '),
            ]
        else:
            self.prompt = [
                ('class:base', '[hbf] '),
                ('class:category', ''),
                ('class:module', ''),
                ('class:pound', '> '),
            ]

    def _list_modules(self):
        """
        Generate modules path and attributes list
        :return: List of available modules
        """
        modules = []
        module_name = "hbfmodules"

        try:
            package = import_module(module_name)
        except ImportError:
            self.logger.print('Unable to find any modules, quit the framework...', Logger.ERROR)
            quit(1)
        for loader, module, is_pkg in pkgutil.walk_packages(package.__path__, prefix=package.__name__ + '.'):
            try:
                imported_module = import_module(module)
                for x in dir(imported_module):
                    obj = getattr(imported_module, x)
                    if inspect.isclass(obj) and issubclass(obj, AModule) and obj is not AModule:
                        module_path = module.replace('hbfmodules.', '').replace('.', '/')
                        modules.append({"path": module_path, "class": obj})
            except ImportError:
                self.logger.print('Error dynamically import package "{}"...'.format(module), Logger.ERROR)
        return modules

    def run(self):
        """
        Main loop, waiting for user input
        :return:
        """
        # TODO: close everything before exit
        # TODO: Improve Ctrl+c handle
        session = PromptSession()
        try:
            while True:
                command = session.prompt(self.prompt, style=self.prompt_style)
                self.dispatcher.handler(self, command)
        except KeyboardInterrupt:
            exit(1)
