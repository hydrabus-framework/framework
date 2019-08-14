import os

from inspect import signature

from hydrabus_framework.core.command.run import run_module
from hydrabus_framework.core.command.show import show
from hydrabus_framework.core.command.set_options import set_options
from hydrabus_framework.core.command.use import use
from hydrabus_framework.core.command.back import back
from hydrabus_framework.core.command.quit import hbf_exit
from hydrabus_framework.core.command.help import hbf_help
from hydrabus_framework.core.command.miniterm import miniterm


class Dispatcher:
    def __init__(self):
        self.commands = [
            {"name": "show", "descr": "modules|options: Displays modules list, or module options", "run": show,
             "arguments": ["options", "modules"]},
            {"name": "help", "descr": "Help menu", "run": hbf_help, "arguments": []},
            {"name": "exit", "descr": "Exit the console", "run": hbf_exit, "arguments": []},
            {"name": "use", "descr": "Load a module by name", "run": use, "arguments": []},
            {"name": "run", "descr": "Run the selected module", "run": run_module, "arguments": []},
            {"name": "back", "descr": "Move back from the current context", "run": back, "arguments": []},
            {"name": "set", "descr": "Sets a context-specific variable to a value", "run": set_options,
             "arguments": []},
            {"name": "miniterm", "descr": "Open a miniterm serial console", "run": miniterm, "arguments": []}
        ]

    def handler(self, hbf_instance, command):
        """
        User console command handler
        :param hbf_instance: Hydrabus framework instance (self)
        :param command: User input
        """
        args = command.split(" ")
        for cmd in self.commands:
            if command.split(" ")[0] == cmd["name"]:
                if len(signature(cmd["run"]).parameters) > 1:
                    cmd["run"](hbf_instance, *args)
                else:
                    cmd["run"](hbf_instance)
                break
        else:
            os.system(command)
