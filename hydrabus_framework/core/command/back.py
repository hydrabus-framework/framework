__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


def back(hbf_instance):
    """
    Move back from the current context
    :param hbf_instance: Hydrabus framework instance (self)
    :return: Nothing
    """
    hbf_instance.current_module = None
    hbf_instance.update_prompt("")
