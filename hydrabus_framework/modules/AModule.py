from abc import ABC, abstractmethod

from hydrabus_framework.utils.logger import Logger


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


class AModule(ABC):
    def __init__(self, hbf_config):
        self.name = None
        self.meta = {
            'name': '',
            'version': '',
            'description': '',
            'author': ''
        }
        self.logger = Logger()
        self.options = []
        self.config = hbf_config

    def __name__(self):
        """
        Simply return the module name
        :return: module name
        """
        return self.name

    def get_option_value(self, option_name):
        """
        Return the value of a specific option.
        :param option_name: The needed option name.
        :return: Value.
        """
        for option in self.options:
            if option["Name"] == option_name:
                return option["Value"]
        else:
            raise UserWarning("Value {} not found in module options".format(option_name))

    def show_options(self):
        """
        Print available options for the module to user console.
        :return: Nothing.
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
        """
        Print meta of the module (author, module name, description).
        :return: Nothing.
        """
        self.logger.handle('Author: {}'.format(self.meta['author']), Logger.HEADER)
        self.logger.handle('Module name: {}, version {}'.format(self.meta['name'], self.meta['version']), Logger.HEADER)
        self.logger.handle('Description: {}'.format(self.meta['description']), Logger.HEADER)

    @abstractmethod
    def run(self):
        """
        Main function.
        :return:
        """
        pass

