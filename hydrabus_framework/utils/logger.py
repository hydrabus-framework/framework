from tabulate import tabulate

from hydrabus_framework.utils.Colors import Colors


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


class Logger:
    """
    The aim of this class is to manage core framework and module printing
    """
    ERROR = 1
    SUCCESS = 2
    INFO = 3
    RESULT = 4
    USER_INTERACT = 5
    HEADER = 6

    def __init__(self):
        self.categories = [
            {"category": 1, "fct": self._print_error},
            {"category": 2, "fct": self._print_success},
            {"category": 3, "fct": self._print_info},
            {"category": 4, "fct": self._print_result},
            {"category": 5, "fct": self._print_user_interact},
            {"category": 6, "fct": self._print_header},
        ]

    def print(self, text, category=None):
        """
        This function print in different color a given string
        :param text: type string, the string to print on the console
        :param category: the message category
        :return:
        """
        for cat in self.categories:
            if cat["category"] == category:
                cat["fct"](text)
                break
        else:
            print(text)

    @staticmethod
    def _print_error(text):
        """
        Beautify error message
        :param text: String, message to be printed
        :return: Nothing
        """
        print("{}[✘]{} {}".format(Colors.FAIL, Colors.ENDC, text))

    @staticmethod
    def _print_success(text):
        """
        Beautify success message
        :param text: String, message to be printed
        :return: Nothing
        """
        print("{}[✔]{} {}".format(Colors.OKGREEN, Colors.ENDC, text))

    @staticmethod
    def _print_info(text):
        """
        Beautify info message
        :param text: String, message to be printed
        :return: Nothing
        """
        print("[*] {}".format(text))

    @staticmethod
    def _print_result(text):
        """
        Beautify result message
        :param text: String, message to be printed
        :return: Nothing
        """
        print("{}[✔]{} {}".format(Colors.OKGREEN, text, Colors.ENDC))

    @staticmethod
    def _print_user_interact(text):
        """
        Beautify needed user's interaction message
        :param text: String, message to be printed
        :return: Nothing
        """
        print("{}[*]{} {}".format(Colors.OKBLUE, text, Colors.ENDC))

    @staticmethod
    def _print_header(text):
        """
        Beautify header message
        :param text: String, message to be printed
        :return: Nothing
        """
        print("{}{}{}".format(Colors.BOLD, text, Colors.ENDC))

    @staticmethod
    def print_tabulate(data, headers):
        """
        Print data in a beautiful tab
        :param data: Array
        :param headers: The headers of array passed
        :return: Nothing
        """
        print("\n{}\n".format(tabulate(data, headers=headers)))
