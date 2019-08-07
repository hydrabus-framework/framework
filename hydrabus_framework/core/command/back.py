__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


def back(hbf_instance):
    """
    Move back from the current context
    :param hbf_instance: Hydrabus framework instance (self)
    :return: Nothing
    """
    if len(hbf_instance.modules_history) > 0:
        previous_module = hbf_instance.modules_history.pop()
        hbf_instance.current_module_name = previous_module["path"]
        hbf_instance.current_module = previous_module["class"]
        hbf_instance.console_completer.words_dic["set"] = hbf_instance.options_list()
    else:
        if hbf_instance.current_module is not None:
            hbf_instance.current_module = None
            hbf_instance.current_module_name = None
            hbf_instance.console_completer.words_dic["set"] = []
