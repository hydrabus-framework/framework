from modules.base import BaseModule


def back(hbf_instance):
    """
    Move back from the current context
    :param hbf_instance: Hydrabus framework instance (self)
    :return:
    """
    hbf_instance.current_module = BaseModule()
    hbf_instance.update_prompt("")
