def set_options(hbf_instance, command):
    """
    Sets a context-specific variable to a value
    :param command: command: string, user seized entry
    :param hbf_instance: Hydrabus framework instance (self)
    :return:
    """
    array_option = command.split(" ")
    if len(array_option) < 3:
        hbf_instance.logger.print("Bad usage", "error")
        hbf_instance.logger.print("Usage: set option_name value", "info")
    else:
        for option in hbf_instance.current_module.options:
            if option["Name"].upper() == array_option[1].upper():
                option["Value"] = array_option[2]
                break
        else:
            hbf_instance.logger.print("option does not exist", "error")
