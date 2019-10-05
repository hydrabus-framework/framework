from hydrabus_framework.modules.AModule import AModule
from hydrabus_framework.utils.logger import Logger


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


def unset_options(hbf_instance, *args):
    """
    Unset a context-specific variable to a value.
    :param args: varargs command options.
    :param hbf_instance: Hydrabus framework instance (self).
    :return: Nothing.
    """
    if len(args) < 2:
        hbf_instance.logger.handle("Bad usage", Logger.ERROR)
        hbf_instance.logger.handle("Usage: unset option_name", Logger.INFO)
    else:
        if isinstance(hbf_instance.current_module, AModule):
            for option in hbf_instance.current_module.options:
                if option["Name"].upper() == args[1].upper():
                    option["Value"] = ""
                    msg = "{} ==> ".format(option["Name"])
                    hbf_instance.logger.handle(msg)
                    break
            else:
                hbf_instance.logger.handle("option does not exist", Logger.ERROR)
