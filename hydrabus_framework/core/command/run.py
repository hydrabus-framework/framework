import traceback
from hydrabus_framework.modules.base import ABaseModule


def run_module(hbf_instance):
    """
    Check all arguments and run the selected module
    :param hbf_instance: hydrabus serial instance
    :return:
    """
    if isinstance(hbf_instance.current_module, ABaseModule):
        ret, err = hbf_instance.current_module.check_args()
        if not ret:
            hbf_instance.logger.print(err, "error")
        try:
            hbf_instance.current_module.run()
        except:
            hbf_instance.logger.print("Error running module", "error")
            traceback.print_exc()
