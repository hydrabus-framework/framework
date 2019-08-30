from hydrabus_framework.utils.logger import Logger


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


def _print_usage(hbf_instance):
    """
    Print use command usage
    :param hbf_instance: Hydrabus framework instance (self)
    :return: Nothing
    """
    hbf_instance.logger.handle("Bad usage", Logger.ERROR)
    hbf_instance.logger.handle("Usage: use <module_name>", Logger.INFO)


def _check_args(hbf_instance, *args):
    """
    Check the length of use commands arguments and its validity
    :param hbf_instance: Hydrabus framework instance (self)
    :param args: vargs (show command argument)
    :return:
    """
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
                if hbf_instance.current_module is not None and hbf_instance.current_module_name != module["path"]:
                    hbf_instance.modules_history.append({"path": hbf_instance.current_module_name,
                                                         "class": hbf_instance.current_module})
                hbf_instance.current_module = module["class"](hbf_instance.config)
                hbf_instance.current_module_name = module["path"]
                for global_option_name, global_option_value in hbf_instance.global_options.items():
                    for module_option in hbf_instance.current_module.options:
                        if global_option_name.upper() == module_option["Name"].upper():
                            module_option["Value"] = global_option_value
                hbf_instance.update_completer_options_list()
                break
        else:
            hbf_instance.logger.handle("module not found", Logger.ERROR)
