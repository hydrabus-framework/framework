__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


def use(hbf_instance, command):
    """
    Method used to select a specific module
    :param command: User input
    :param hbf_instance: Hydrabus framework instance (self)
    """
    if len(command.split(" ")) < 2:
        print("usage")
    else:
        for module in hbf_instance.modules:
            if module["path"] == command.split(" ")[1]:
                hbf_instance.current_module = module["class"]()
                hbf_instance.update_prompt(module["path"])
                break
        else:
            print("module not found")
