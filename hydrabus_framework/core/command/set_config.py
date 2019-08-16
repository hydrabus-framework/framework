from hydrabus_framework.utils.logger import Logger


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


def set_config(hbf_instance, *args):
    """
    Sets a config variable to a value
    :param args: varargs command options
    :param hbf_instance: Hydrabus framework instance (self)
    :return: Nothing
    """
    if len(args) < 4:
        hbf_instance.logger.handle("Bad usage", Logger.ERROR)
        hbf_instance.logger.handle("Usage: setc CATEGORY key value", Logger.INFO)
    else:
        if not hbf_instance.config.has_section(args[1]):
            hbf_instance.logger.handle("Config section '{}' does not exist".format(args[1]), Logger.ERROR)
        else:
            if not hbf_instance.config.has_option(args[1], args[2]):
                hbf_instance.logger.handle("Value '{}' does not exist in section '{}'"
                                           .format(args[2], args[1]), Logger.ERROR)
            else:
                hbf_instance.config[args[1]][args[2]] = args[3]
