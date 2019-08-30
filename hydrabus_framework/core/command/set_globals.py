from hydrabus_framework.modules.AModule import AModule
from hydrabus_framework.utils.logger import Logger


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


def set_globals(hbf_instance, *args):
    """
    Set a global variable to a value
    :param args: varargs command options
    :param hbf_instance: Hydrabus framework instance (self)
    :return: Nothing
    """
    if len(args) < 3:
        hbf_instance.logger.handle("Bad usage", Logger.ERROR)
        hbf_instance.logger.handle("Usage: setg option_name value", Logger.INFO)
    else:
        hbf_instance.global_options.update({args[1].upper(): args[2]})
        msg = "{} ==> {}".format(args[1].upper(), args[2])
        hbf_instance.logger.handle(msg)
        if isinstance(hbf_instance.current_module, AModule):
            for option in hbf_instance.current_module.options:
                if option["Name"].upper() == args[1].upper():
                    option["Value"] = args[2]
