import traceback

from hydrabus_framework.modules.amodule import AModule


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
            hbf_instance.logger.print(err, "error")
        try:
            hbf_instance.current_module.run()
        except:
            hbf_instance.logger.print("Error running module", "error")
            traceback.print_exc()
