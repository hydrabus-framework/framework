import inspect
import sys
import os
from modules.base import BaseModule
from importlib import import_module
from modules import base
from prompt_toolkit.shortcuts import PromptSession
from prompt_toolkit.styles import Style
from tabulate import tabulate
from core.helper import Helper


class HydraFramework:
    """
    Framework core engine
    """
    def __init__(self):
        self.helper = Helper()
        self.app_path = sys.path[0]
        self._home = ''
        self.module_command = ["set", "run", "unset"]
        self.generic_command = ["use", "help", "exit", "back", "show"]
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
        self.current_module = base.BaseModule()
        self.modules = self.__list_modules()
        self.command = [
            {"name": "show", "descr": "modules|options: Displays modules list, or module options", "run": self.show},
            {"name": "help", "descr": "Help menu", "run": self.help},
            {"name": "exit", "descr": "Exit the console", "run": self._exit},
            {"name": "use", "descr": "Load a module by name", "run": self.use},
            {"name": "run", "descr": "Run the selected module", "run": self.run_module},
            {"name": "back", "descr": "Move back from the current context", "run": self.back},
            {"name": "set", "descr": "Sets a context-specific variable to a value", "run": self.set}
        ]

    def _print_tabulate(self, data, headers):
        print()
        print(tabulate(data, headers=headers))
        print()

    def set(self, command):
        """
        Sets a context-specific variable to a value
        TODO: check if another method is possible instead of using an index variable
        """
        array_option = command.split(" ")
        if len(array_option) < 3:
            self.helper.print_error("Bad usage")
            self.helper.print_info("Usage: set option_name value")
        else:
            for option in self.current_module.options:
                if option["Name"] == array_option[1]:
                    option["Value"] = array_option[2]
                    break
            else:
                self.helper.print_error("option does not exist")

    def back(self):
        """
        back function: Move back from the current context
        """
        self.current_module = base.BaseModule()
        self.update_prompt("")

    def run_module(self):
        """
        Check all arguments and run the selected module
        """
        ret, err = self.current_module.check_args()
        if not ret:
            self.log.print_error(err)
        self.current_module.check_args()
        try:
            self.current_module.run()
        except:
            self.helper.print_error("Error running module")

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

    def use(self, command):
        """
        Method used to select a specific module
        :param command: User input
        """
        if len(command.split(" ")) < 2:
            print("usage")
        else:
            for module in self.modules:
                if module["path"] == command.split(" ")[1]:
                    self.current_module = module["class"]()
                    self.update_prompt(module["path"])
                    break
            else:
                print("module not found")

    def _exit(self):
        exit(0)

    def help(self):
        """
        Print framework help on the console
        """
        print()
        print("Core Commands")
        print("=============")
        formatted_commands = []
        for cmd in self.command:
            formatted_commands.append(
                {
                    "Command": cmd["name"],
                    "Description": cmd["descr"]
                }
            )
        self._print_tabulate(formatted_commands, headers={"name": "Name", "descr": "Description"})

    def show(self, command):
        """
        Displays modules list, or module options. Depending on arguments
        :param command:
        """
        # TODO: print by category separately
        try:
            if command.split(" ")[1] == "modules":
                formatted_modules = []
                print("================")
                print("| Modules list |")
                print("================")
                for module in self.modules:
                    formatted_modules.append({"Path": module["path"],
                                              "Description": module["class"]().get_description()})
                self._print_tabulate(formatted_modules, headers={"Path": "Path", "Description": "Description"})
            else:
                if self.current_module.__name__ != "BaseModule":
                    if command.split(" ")[1] == "options":
                        self.current_module.show_options()
        except IndexError:
            print("Usage: show modules|options")

    def __list_modules(self):
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
        # TODO: check command that need arguments, else run without
        for cmd in self.command:
            if command.split(" ")[0] == cmd["name"]:
                if len(inspect.getfullargspec(cmd["run"])[0]) > 1:
                    cmd["run"](command)
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
