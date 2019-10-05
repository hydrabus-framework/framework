from hydrabus_framework.utils.logger import Logger


class Validator:
    """
    Class allowing to check module options (if set and if format is ok).
    """
    def __init__(self):
        self.logger = Logger()

    def _args_validator(self, options_dict):
        """
        Check arguments type validity & Convert to the specified format.
        :param options_dict: module options dictionary
        :return: Bool
        """
        for option in options_dict:
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

    def check_args(self, options_dict):
        """
        Check if all arguments are defined by user, or set default value if available.
        :param options_dict: module options dictionary
        :return: Bool
        """
        if len(options_dict) > 0:
            for option in options_dict:
                if option["Required"] and option["Value"] == "":
                    if option["Default"] == "":
                        self.logger.handle("OptionValidateError: The following options failed to validate: {}."
                                           .format(option["Name"]), Logger.ERROR)
                        return False
                    else:
                        option["Value"] = option["Default"]
            if not self._args_validator(options_dict):
                return False
        return True
