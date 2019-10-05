from hydrabus_framework.modules.AModule import AModule
from hydrabus_framework.utils.logger import Logger


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


def _print_usage(hbf_instance):
    """
    Print show command usage
    :param hbf_instance: Hydrabus framework instance (self)
    :return: Nothing
    """
    hbf_instance.logger.handle("Bad usage", Logger.ERROR)
    hbf_instance.logger.handle("Usage: show modules|options|config|global", Logger.INFO)


def _check_args(hbf_instance, *args):
    """
    Check the length of show commands arguments and its validity.
    :param hbf_instance: Hydrabus framework instance (self).
    :param args: vargs (show command argument).
    :return: Bool.
    """
    if len(args) < 2:
        _print_usage(hbf_instance)
        return False
    if args[1] not in ["modules", "options", "config", "global"]:
        _print_usage(hbf_instance)
        return False
    return True


def show(hbf_instance, *args):
    """
    Displays modules list, module options or global config. Depending on arguments.
    :param args: varargs command options.
    :param hbf_instance: Hydrabus framework instance (self).
    :return: Nothing.
    """
    # TODO: print by protocol separately
    if _check_args(hbf_instance, *args):
        if args[1] == "modules":
            print("\n================")
            print("| Modules list |")
            print("================\n")
            formatted_modules = []
            for module in hbf_instance.modules:
                formatted_modules.append({"Path": module["path"],
                                          "Description": module["class"](hbf_instance.config).meta["description"]})
            hbf_instance.logger.print_tabulate(formatted_modules,
                                               headers={"Path": "Path", "Description": "Description"})
        elif args[1] == "config":
            print("\n================")
            print("|    Config    |")
            print("================\n")
            for section in hbf_instance.config:
                print("\n[{}]".format(section))
                for key in hbf_instance.config[section]:
                    print("{} = {}".format(key, hbf_instance.config[section][key]))
        elif args[1] == "global":
            print("\n==================")
            print("| Global options |")
            print("==================\n")
            for key, value in hbf_instance.global_options.items():
                print(f"{key} ==> {value}")
        else:
            if isinstance(hbf_instance.current_module, AModule):
                hbf_instance.current_module.show_options()
