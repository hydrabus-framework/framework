from hydrabus_framework.modules.AModule import AModule
from hydrabus_framework.utils.logger import Logger


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


def _print_usage(hbf_instance):
    hbf_instance.logger.handle("Bad usage", Logger.ERROR)
    hbf_instance.logger.handle("Usage: show modules|options", Logger.INFO)


def _check_args(hbf_instance, *args):
    if len(args) < 2:
        _print_usage(hbf_instance)
        return False
    if args[1] not in ["modules", "options"]:
        _print_usage(hbf_instance)
        return False
    return True


def show(hbf_instance, *args):
    """
    Displays modules list, or module options. Depending on arguments
    :param args: varargs command options
    :param hbf_instance: Hydrabus framework instance (self)
    :return:
    """
    # TODO: print by category separately
    if _check_args(hbf_instance, *args):
        if args[1] == "modules":
            formatted_modules = []
            print("================")
            print("| Modules list |")
            print("================")
            for module in hbf_instance.modules:
                formatted_modules.append({"Path": module["path"],
                                          "Description": module["class"]().get_description()})
            hbf_instance.logger.print_tabulate(formatted_modules,
                                               headers={"Path": "Path", "Description": "Description"})
        else:
            if isinstance(hbf_instance.current_module, AModule):
                hbf_instance.current_module.show_options()
