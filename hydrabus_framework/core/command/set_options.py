from hydrabus_framework.modules.AModule import AModule
from hydrabus_framework.utils.logger import Logger


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


def set_options(hbf_instance, *args):
    """
    Sets a context-specific variable to a value
    :param args: varargs command options
    :param hbf_instance: Hydrabus framework instance (self)
    :return: Nothing
    """
    if len(args) < 3:
        hbf_instance.logger.handle("Bad usage", Logger.ERROR)
        hbf_instance.logger.print("Usage: set option_name value", Logger.INFO)
    else:
        if isinstance(hbf_instance.current_module, AModule):
            for option in hbf_instance.current_module.options:
                if option["Name"].upper() == args[1].upper():
                    option["Value"] = args[2]
                    msg = "{} ==> {}".format(option["Name"], args[2])
                    hbf_instance.logger.print(msg)
                    break
            else:
                hbf_instance.logger.print("option does not exist", Logger.ERROR)
