import inspect
import pkgutil
import sys

from importlib import import_module
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.styles import Style

from hydrabus_framework.core.Dispatcher import Dispatcher
from hydrabus_framework.modules.AModule import AModule
from hydrabus_framework.utils.logger import Logger
from hydrabus_framework.utils.NestedCompleter import NestedCompleter


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


class HydraFramework:
    """
    Framework core engine
    """
    def __init__(self):
        self.logger = Logger()
        self.app_path = sys.path[0]
        self.current_module = None
        self.current_module_name = None
        self.dispatcher = Dispatcher()
        self.console_completer = NestedCompleter(self.simple_cmd_dict(), ignore_case=True)
        self.modules = self._list_modules()
        self.modules_history = []
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

    def update_prompt(self):
        """
        Update the user prompt
        :param module_name: The current module name
        """
        if self.current_module_name is not None:
            category = self.current_module_name.split("/")[0]
            module = self.current_module_name.split("/")[1]
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
            self.logger.handle('Unable to find any modules, quit the framework...', Logger.ERROR)
            quit(1)
        for loader, module, is_pkg in pkgutil.walk_packages(package.__path__, prefix=package.__name__ + '.'):
            try:
                imported_module = import_module(module)
                for x in dir(imported_module):
                    obj = getattr(imported_module, x)
                    if inspect.isclass(obj) and issubclass(obj, AModule) and obj is not AModule:
                        module_path = module.replace('hbfmodules.', '').replace('.', '/')
                        modules.append({"path": module_path, "class": obj})
                        self.console_completer.words_dic["use"].append(module_path)
            except ImportError:
                self.logger.handle('Error dynamically import package "{}"...'.format(module), Logger.ERROR)
        return modules

    def simple_cmd_dict(self):
        commands = {}
        for command in self.dispatcher.commands:
            commands.update({command["name"]: command["arguments"]})
        return commands

    def options_list(self):
        options = []
        if self.current_module is not None:
            for option in self.current_module.options:
                options.append(option["Name"])
        return options

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
                command = session.prompt(self.prompt, style=self.prompt_style, completer=self.console_completer,
                                         complete_while_typing=False)
                self.dispatcher.handler(self, command)
                self.update_prompt()
        except KeyboardInterrupt:
            exit(1)
