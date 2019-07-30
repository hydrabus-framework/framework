import traceback

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
        ret, err = hbf_instance.current_module.check_args()
        if not ret:
            hbf_instance.logger.handle(err, Logger.ERROR)
        try:
            hbf_instance.current_module.run()
        except:
            hbf_instance.logger.handle("Error running module", Logger.ERROR)
            traceback.print_exc()
