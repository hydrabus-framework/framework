import inspect
import os

from hydrabus_framework.core.command.run import run_module
from hydrabus_framework.core.command.show import show
from hydrabus_framework.core.command.set_options import set_options
from hydrabus_framework.core.command.use import use
from hydrabus_framework.core.command.back import back
from hydrabus_framework.core.command.quit import hbf_exit
from hydrabus_framework.core.command.help import hbf_help


class Dispatcher:
    def __init__(self):
        self.commands = [
            {"name": "show", "descr": "modules|options: Displays modules list, or module options", "run": show},
            {"name": "help", "descr": "Help menu", "run": hbf_help},
            {"name": "exit", "descr": "Exit the console", "run": hbf_exit},
            {"name": "use", "descr": "Load a module by name", "run": use},
            {"name": "run", "descr": "Run the selected module", "run": run_module},
            {"name": "back", "descr": "Move back from the current context", "run": back},
            {"name": "set", "descr": "Sets a context-specific variable to a value", "run": set_options}
        ]

    def handler(self, hbf_instance, command):
        """
        User console command handler
        :param hbf_instance: Hydrabus framework instance (self)
        :param command: User input
        """
        for cmd in self.commands:
            if command.split(" ")[0] == cmd["name"]:
                if len(inspect.getfullargspec(cmd["run"])[0]) == 2:
                    cmd["run"](hbf_instance, command)
                elif len(inspect.getfullargspec(cmd["run"])[0]) == 1:
                    cmd["run"](hbf_instance)
                else:
                    cmd["run"]()
                break
        else:
            os.system(command)
