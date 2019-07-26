from hydrabus_framework.modules.base import ABaseModule


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


def show(hbf_instance, command):
    """
    Displays modules list, or module options. Depending on arguments
    :param command: string, user seized entry
    :param hbf_instance: Hydrabus framework instance (self)
    :return:
    """
    # TODO: print by category separately
    try:
        if command.split(" ")[1] == "modules":
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
            if isinstance(hbf_instance.current_module, ABaseModule):
                if command.split(" ")[1] == "options":
                    hbf_instance.current_module.show_options()
    except IndexError:
        print("Usage: show modules|options")
