from hydrabus_framework.core.logger import Logger


def show(hbf_instance, command):
    """
    Displays modules list, or module options. Depending on arguments
    :param command: string, user seized entry
    :param hbf_instance: Hydrabus framework instance (self)
    :return:
    """
    # TODO: print by category separately
    logger = Logger()
    try:
        if command.split(" ")[1] == "modules":
            formatted_modules = []
            print("================")
            print("| Modules list |")
            print("================")
            for module in hbf_instance.modules:
                formatted_modules.append({"Path": module["path"],
                                          "Description": module["class"]().get_description()})
            logger.print_tabulate(formatted_modules, headers={"Path": "Path", "Description": "Description"})
        else:
            if hbf_instance.current_module.__name__ != "BaseModule":
                if command.split(" ")[1] == "options":
                    hbf_instance.current_module.show_options()
    except IndexError:
        print("Usage: show modules|options")
