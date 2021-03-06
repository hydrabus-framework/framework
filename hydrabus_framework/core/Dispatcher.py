import os

from inspect import signature

from hydrabus_framework.core.command.back import back
from hydrabus_framework.core.command.help import hbf_help
from hydrabus_framework.core.command.miniterm import miniterm
from hydrabus_framework.core.command.quit import hbf_exit
from hydrabus_framework.core.command.reset_hb import reset_hb
from hydrabus_framework.core.command.run import run_module
from hydrabus_framework.core.command.save_config import save_config
from hydrabus_framework.core.command.set_config import set_config
from hydrabus_framework.core.command.set_globals import set_globals
from hydrabus_framework.core.command.set_options import set_options
from hydrabus_framework.core.command.show import show
from hydrabus_framework.core.command.unset_globals import unset_globals
from hydrabus_framework.core.command.unset_options import unset_options
from hydrabus_framework.core.command.use import use


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


class Dispatcher:
    def __init__(self):
        self.commands = [
            {"name": "?", "descr": "Alias for help menu", "run": hbf_help, "arguments": {}},
            {"name": "help", "descr": "Help menu", "run": hbf_help, "arguments": {}},
            {"name": "show", "descr": "modules|options|config|global: Displays modules list, "
                                      "module options, global configuration or global options", "run": show,
                                      "arguments": {"options", "modules", "config", "global"}},
            {"name": "use", "descr": "Load a module by name", "run": use, "arguments": {}},
            {"name": "run", "descr": "Run the selected module", "run": run_module, "arguments": {}},
            {"name": "back", "descr": "Move back from the current context", "run": back, "arguments": {}},
            {"name": "set", "descr": "Set a context-specific variable to a value", "run": set_options,
             "arguments": {}},
            {"name": "unset", "descr": "Unset a context-specific variable", "run": unset_options, "arguments": {}},
            {"name": "setg", "descr": "Set a global variable to a value", "run": set_globals, "arguments": {}},
            {"name": "unsetg", "descr": "Unset a global variable", "run": unset_globals, "arguments": {}},
            {"name": "setc", "descr": "Set a config key to a value", "run": set_config, "arguments": {}},
            {"name": "save", "descr": "Save the current config into hbf.cfg file", "run": save_config, "arguments": {}},
            {"name": "miniterm", "descr": "Open a miniterm serial console", "run": miniterm, "arguments": {}},
            {"name": "reset", "descr": "Reset hydrabus in main mode", "run": reset_hb, "arguments": {}},
            {"name": "exit", "descr": "Exit the console", "run": hbf_exit, "arguments": {}}
        ]

    def handle(self, hbf_instance, command):
        """
        User console command handler.
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
