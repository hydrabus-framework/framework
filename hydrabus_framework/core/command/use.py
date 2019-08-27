from hydrabus_framework.utils.logger import Logger


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


def _print_usage(hbf_instance):
    hbf_instance.logger.handle("Bad usage", Logger.ERROR)
    hbf_instance.logger.handle("Usage: use <module_name>", Logger.INFO)


def _check_args(hbf_instance, *args):
    if len(args) < 2:
        _print_usage(hbf_instance)
        return False
    if args[1] == "":
        _print_usage(hbf_instance)
        return False
    return True


def use(hbf_instance, *args):
    """
    Method used to select a specific module
    :param args: varargs command options
    :param hbf_instance: Hydrabus framework instance (self)
    :return: Nothing
    """
    if _check_args(hbf_instance, *args):
        for module in hbf_instance.modules:
            if module["path"] == args[1]:
                if hbf_instance.current_module is not None:
                    hbf_instance.modules_history.append({"path": module["path"], "class": module["class"]()})
                hbf_instance.current_module = module["class"]()
                hbf_instance.current_module_name = module["path"]
                hbf_instance.update_completer_options_list()
                break
        else:
            hbf_instance.logger.handle("module not found", Logger.ERROR)
