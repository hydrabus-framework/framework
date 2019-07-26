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
        self.categories = [
            {"category": "error", "fct": self._print_error},
            {"category": "success", "fct": self._print_success},
            {"category": "info", "fct": self._print_info},
            {"category": "result", "fct": self._print_result},
            {"category": "user", "fct": self._print_user_interact},
            {"category": "header", "fct": self._print_header},
        ]

    def print(self, text, category=None):
        """
        This function print in different color a given string
        :param text: type string, the string to print on the console
        :param category: the message category
        :return:
        """
        for cat in self.categories:
            if cat == category:
                cat["fct"](text)
                break
        else:
            print(text)

    def _print_error(self, text):
        print("{}[✘]{} {}".format(self.FAIL, self.ENDC, text))

    def _print_success(self, text):
        print("{}[✔]{} {}".format(self.OKGREEN, self.ENDC, text))

    def _print_info(self, text):
        print("[*] {}".format(text))

    def _print_result(self, text):
        print("{}[✔]{} {}".format(self.OKGREEN, text, self.ENDC))

    def _print_user_interact(self, text):
        print("{}[*]{} {}".format(self.OKBLUE, text, self.ENDC))

    def _print_header(self, text):
        print("{}{}{}".format(self.BOLD, text, self.ENDC))

    @staticmethod
    def print_tabulate(data, headers):
        """
        Print data in a beautiful tab
        :param data: Array
        :param headers: The headers of array passed
        :return:
        """
        print("\n{}\n".format(tabulate(data, headers=headers)))
