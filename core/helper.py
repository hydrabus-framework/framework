class Helper:
    def __init__(self):
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'

    def print_error(self, text):
        print("{}[!]{} {}".format(self.FAIL, self.ENDC, text))

    def print_success(self, text):
        print("{}[+]{} {}".format(self.OKGREEN, self.ENDC, text))

    def print_info(self, text):
        print("[*] {}".format(text))

    def print_success_result(self, text):
        print("{}[+++]{} {}".format(self.OKGREEN, text, self.ENDC))

    def print_user_interaction(self, text):
        print("{}[*]{} {}".format(self.OKBLUE, text, self.ENDC))
