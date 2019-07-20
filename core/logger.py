from tabulate import tabulate

class Logger:
    def __init__(self):
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'

    def print(self, text, category):
        """
        This function print in different color a given string
        :param text: type string, the string to print on the console
        :param category: the message category
        :return:
        """
        if category == "error":
            print("{}[!]{} {}".format(self.FAIL, self.ENDC, text))
        if category == "success":
            print("{}[+]{} {}".format(self.OKGREEN, self.ENDC, text))
        if category == "info":
            print("[*] {}".format(text))
        if category == "result":
            print("{}[+++]{} {}".format(self.OKGREEN, text, self.ENDC))
        if category == "user":
            print("{}[*]{} {}".format(self.OKBLUE, text, self.ENDC))

    def print_tabulate(self, data, headers):
        """
        Print data in a beautiful tab
        :param data: Array
        :param headers: The headers of array passed
        :return:
        """
        print()
        print(tabulate(data, headers=headers))
        print()
