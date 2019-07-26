import inspect
import os
import pkgutil
import sys

from importlib import import_module
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.styles import Style

from hydrabus_framework.core.logger import Logger
from hydrabus_framework.core.command.run import run_module
from hydrabus_framework.core.command.show import show
from hydrabus_framework.core.command.set_options import set_options
from hydrabus_framework.core.command.use import use
from hydrabus_framework.core.command.back import back
from hydrabus_framework.core.command.quit import hbf_exit
from hydrabus_framework.core.command.help import hbf_help
from hydrabus_framework.modules.base import ABaseModule


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
        self.prompt_style = Style.from_dict({
            # User input (default text).
            '': '#ffffff',

            # Prompt.
            'username': '#3399ff',
            'pound': '#3399ff',
            'path': '#ff0000 bold',
        })
        self.prompt = [
            ('class:username', '[hbf] '),
            ('class:path', ''),
            ('class:pound', '> '),
        ]
        self.command = [
            {"name": "show", "descr": "modules|options: Displays modules list, or module options", "run": show},
            {"name": "help", "descr": "Help menu", "run": hbf_help},
            {"name": "exit", "descr": "Exit the console", "run": hbf_exit},
            {"name": "use", "descr": "Load a module by name", "run": use},
            {"name": "run", "descr": "Run the selected module", "run": run_module},
            {"name": "back", "descr": "Move back from the current context", "run": back},
            {"name": "set", "descr": "Sets a context-specific variable to a value", "run": set_options}
        ]

    def update_prompt(self, module_name):
        """
        Update the user prompt
        :param module_name: The current module name
        """
        if module_name != "":
            self.prompt = [
                ('class:username', '[hbf] '),
                ('class:path', '({})'.format(module_name)),
                ('class:pound', '> '),
            ]
        else:
            self.prompt = [
                ('class:username', '[hbf] '),
                ('class:path', ''),
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
            for loader, module, is_pkg in pkgutil.walk_packages(package.__path__, prefix=package.__name__ + '.'):
                imported_module = import_module(module)
                for x in dir(imported_module):
                    obj = getattr(imported_module, x)
                    if inspect.isclass(obj) and issubclass(obj, ABaseModule) and obj is not ABaseModule:
                        module_path = module.replace('hbfmodules.', '').replace('.', '/')
                        modules.append({"path": module_path, "class": obj})
            return modules
        except ImportError:
            self.logger.print('Error dynamically import package "{}"...'.format(module_name), "error")

    def handler(self, command):
        """
        User console command handler
        :param command: User input
        """
        for cmd in self.command:
            if command.split(" ")[0] == cmd["name"]:
                if len(inspect.getfullargspec(cmd["run"])[0]) == 2:
                    cmd["run"](self, command)
                elif len(inspect.getfullargspec(cmd["run"])[0]) == 1:
                    cmd["run"](self)
                else:
                    cmd["run"]()
                break
        else:
            os.system(command)

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
                self.handler(command)
        except KeyboardInterrupt:
            exit(1)
