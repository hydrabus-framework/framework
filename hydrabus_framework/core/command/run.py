import traceback

from hydrabus_framework.core.utils.Validator import Validator
from hydrabus_framework.modules.AModule import AModule
from hydrabus_framework.utils.logger import Logger


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


def run_module(hbf_instance):
    """
    Check all arguments and run the selected module
    :param hbf_instance: Hydrabus framework instance (self)
    :return: Nothing
    """
    if isinstance(hbf_instance.current_module, AModule):
        ret = Validator().check_args(hbf_instance.current_module.options)
        if ret:
            try:
                hbf_instance.current_module.run()
            except KeyboardInterrupt:
                pass
            except:
                hbf_instance.logger.handle("Error running module", Logger.ERROR)
                traceback.print_exc()
