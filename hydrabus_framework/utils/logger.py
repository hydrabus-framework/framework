import codecs

from tabulate import tabulate
from sys import stdout

from hydrabus_framework.utils.Colors import Colors


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


class Progress:
    """
    Progress logger is used to dynamically print records
    """
    def __init__(self, header=''):
        self.header = header
        self.full_msg = ''

    def status(self, msg):
        """
        Dynamically print character on the same line by calling it multiple time
        :param msg:
        :return:
        """
        # if msg is a white character, convert it to its hex representation
        if msg.isspace() and msg != " ":
            self.full_msg += '0x{}'.format(codecs.encode(bytes(msg, 'utf-8'), 'hex').decode())
        else:
            self.full_msg += msg
        print('{}: {}'.format(self.header, self.full_msg), end='\r', flush=True)

    def stop(self):
        if self.full_msg == '':
            print(end='', flush=False)
        else:
            print(flush=False)


class Logger:
    """
    The aim of this class is to manage core framework and module printing
    """
    DEFAULT = 0
    ERROR = 1
    SUCCESS = 2
    INFO = 3
    RESULT = 4
    USER_INTERACT = 5
    HEADER = 6

    def __init__(self):
        self.categories = [
            self._print_default,
            self._print_error,
            self._print_success,
            self._print_info,
            self._print_result,
            self._print_user_interact,
            self._print_header
        ]

    def handle(self, text, level=DEFAULT):
        """
        This function print in different color a given string
        :param text: type string, the string to print on the console
        :param level: the message category
        :return:
        """
        self.categories[level](text) if (level < len(self.categories)) else self.categories[self.DEFAULT](text)

    @staticmethod
    def _print_default(text):
        """
        Print without style
        :param text: String, message to be printed
        :return: Nothing
        """
        print(text)

    @staticmethod
    def _print_error(text):
        """
        Beautify error message
        :param text: String, message to be printed
        :return: Nothing
        """
        print("{}[✘]{} {}".format(Colors.FAIL.value, Colors.ENDC.value, text))

    @staticmethod
    def _print_success(text):
        """
        Beautify success message
        :param text: String, message to be printed
        :return: Nothing
        """
        print("{}[✔]{} {}".format(Colors.OKGREEN.value, Colors.ENDC.value, text))

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
        print("{}[✔]{} {}".format(Colors.OKGREEN.value, text, Colors.ENDC.value))

    @staticmethod
    def _print_user_interact(text):
        """
        Beautify needed user's interaction message
        :param text: String, message to be printed
        :return: Nothing
        """
        print("{}[*]{} {}".format(Colors.OKBLUE.value, text, Colors.ENDC.value))

    @staticmethod
    def _print_header(text):
        """
        Beautify header message
        :param text: String, message to be printed
        :return: Nothing
        """
        print("{}{}{}".format(Colors.BOLD.value, text, Colors.ENDC.value))

    @staticmethod
    def print_tabulate(data, headers):
        """
        Print data in a beautiful tab
        :param data: Array
        :param headers: The headers of array passed
        :return: Nothing
        """
        print("\n{}\n".format(tabulate(data, headers=headers)))

    @staticmethod
    def progress(header):
        """
        Creates a new progress logger
        :return: Progress class instance
        """
        return Progress(header)

