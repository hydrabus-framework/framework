import inspect
import sys
import os
from modules.base import BaseModule
from importlib import import_module
from modules import base
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.styles import Style
from core.logger import Logger
from core.command.run import run_module
from core.command.show import show
from core.command.set_options import set_options
from core.command.use import use
from core.command.back import back
from core.command.quit import hbf_exit
from core.command.help import hbf_help


class HydraFramework:
    """
    Framework core engine
    """
    def __init__(self):
        self.logger = Logger()
        self.app_path = sys.path[0]
        self._home = ''
        self.current_module = base.BaseModule()
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
        :return:
        """
        modules = []
        current_directory = os.path.dirname(self.app_path + "/modules/")
        submodule_dirs = [d for d in os.listdir(current_directory) if
                          os.path.isdir(os.path.join(current_directory, d)) and "__" not in d]

        for module_dir in submodule_dirs:
            files = [f for f in os.listdir(os.path.join(current_directory, module_dir)) if
                     os.path.isfile(os.path.join(current_directory, module_dir, f))]
            for file in files:
                module = import_module("modules.{}.{}".format(module_dir, file.split('.')[0]))
                for x in dir(module):
                    obj = getattr(module, x)
                    if inspect.isclass(obj) and issubclass(obj, BaseModule) and obj is not BaseModule:
                        modules.append({"path": os.path.join(module_dir, file.split('.')[0]), "class": obj})
        return modules

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
        """
        # TODO: close everything before exit
        session = PromptSession()
        try:
            while True:
                command = session.prompt(self.prompt, style=self.prompt_style)
                self.handler(command)
        except KeyboardInterrupt:
            exit(1)
