from abc import ABC, abstractmethod
from hydrabus_framework.utils.logger import Logger
from tabulate import tabulate


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


class AModule(ABC):
    def __init__(self):
        self.logger = Logger()
        self.name = None
        self.description = None
        self.options = []

    def __name__(self):
        return self.name

    def check_args(self):
        """
        Check if all arguments are defined by user, or set default value if available
        TODO: check type
        :return: Bool, err
        """
        if len(self.options) > 0:
            for option in self.options:
                if option["Required"] and option["Value"] == "":
                    if option["Default"] == "":
                        err = "OptionValidateError: The following options failed to validate: {}."\
                            .format(option["name"])
                        return False, err
                    else:
                        option["Value"] = option["Default"]
        return True, ""

    def get_option_value(self, option_name):
        """
        Return the value of a specific option
        :param option_name: The needed option name
        :return: Bool, Value
        """
        for option in self.options:
            if option["Name"] == option_name:
                return True, option["Value"]
        return False, ""

    def show_options(self):
        """
        Print available options for the module to user console
        :return: Nothing
        """
        formatted_options = []
        if len(self.options) > 0:
            print(self.get_description())
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
            print("\n{}\n".format(tabulate(formatted_options, headers={"Name": "Name", "Description": "Description",
                                                                       "Value": "Value", "Required": "Required"})))

    def get_description(self):
        return self.description

    @abstractmethod
    def run(self):
        pass
