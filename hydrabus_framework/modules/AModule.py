from abc import ABC, abstractmethod

from hydrabus_framework.utils.logger import Logger


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


class AModule(ABC):
    def __init__(self):
        self.name = None
        self.meta = {
            'name': '',
            'version': '',
            'description': '',
            'author': ''
        }
        self.logger = Logger()
        self.options = []

    def __name__(self):
        return self.name

    def _args_validator(self):
        """
        Check arguments type validity & Convert to the specified format
        :return: Bool
        """
        for option in self.options:
            try:
                if option["Type"] == "int":
                    if not isinstance(option["Value"], int):
                        option["Value"] = int(option["Value"], 10)
                if option["Type"] == "bool":
                    if not isinstance(option["Value"], bool):
                        if str(option["Value"]).upper() == "FALSE":
                            option["Value"] = False
                        elif str(option["Value"]).upper() == "TRUE":
                            option["Value"] = True
                        else:
                            raise ValueError
                if option["Value"] == "None":
                    option["Value"] = None
            except ValueError:
                self.logger.handle("Value error: {} is not a member of {}".format(option["Name"], option["Type"]))
                return False
        return True

    def check_args(self):
        """
        Check if all arguments are defined by user, or set default value if available
        :return: Bool
        """
        if len(self.options) > 0:
            for option in self.options:
                if option["Required"] and option["Value"] == "":
                    if option["Default"] == "":
                        self.logger.handle("OptionValidateError: The following options failed to validate: {}."
                                           .format(option["name"]), Logger.ERROR)
                        return False
                    else:
                        option["Value"] = option["Default"]
            if not self._args_validator():
                return False
        return True

    def get_option_value(self, option_name):
        """
        Return the value of a specific option
        :param option_name: The needed option name
        :return: Value
        """
        for option in self.options:
            if option["Name"] == option_name:
                return option["Value"]
        else:
            raise UserWarning("Value {} not found in module options".format(option_name))

    def show_options(self):
        """
        Print available options for the module to user console
        :return: Nothing
        """
        formatted_options = []
        if len(self.options) > 0:
            self.print_meta()
            for option in self.options:
                if option["Default"] != "" and option["Value"] == "":
                    formatted_options.append(
                        {
                            'Name': option["Name"],
                            'Value': option["Default"],
                            'Required': option["Required"],
                            'Description': option["Description"]
                        }
                    )
                else:
                    formatted_options.append(
                        {
                            'Name': option["Name"],
                            'Value': option["Value"],
                            'Required': option["Required"],
                            'Description': option["Description"]
                        }
                    )
            self.logger.print_tabulate(formatted_options, headers={"Name": "Name", "Description": "Description",
                                                                   "Value": "Value", "Required": "Required"})

    def print_meta(self):
        self.logger.handle('Author: {}'.format(self.meta['author']), Logger.HEADER)
        self.logger.handle('Module name: {}, version {}'.format(self.meta['name'], self.meta['version']), Logger.HEADER)
        self.logger.handle('Description: {}'.format(self.meta['description']), Logger.HEADER)

    @abstractmethod
    def run(self):
        pass

