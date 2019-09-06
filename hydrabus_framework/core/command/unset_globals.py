from hydrabus_framework.utils.logger import Logger


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


def unset_globals(hbf_instance, *args):
    """
    Unset a global variable
    :param args: varargs command options
    :param hbf_instance: Hydrabus framework instance (self)
    :return: Nothing
    """
    if len(args) < 2:
        hbf_instance.logger.handle("Bad usage", Logger.ERROR)
        hbf_instance.logger.handle("Usage: unsetg option_name", Logger.INFO)
    else:
        try:
            hbf_instance.global_options.pop(args[1].upper())
            msg = "'{}' successfully unset".format(args[1].upper())
            hbf_instance.logger.handle(msg)
            hbf_instance.update_completer_global_options_list()
        except KeyError:
            hbf_instance.logger.handle("'{}' is not declared as global variable".format(args[1]), Logger.ERROR)

