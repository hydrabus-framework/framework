import traceback
from hydrabus_framework.core.logger import Logger


def run_module(hbf_instance):
    """
    Check all arguments and run the selected module
    :param current_module: Class, Current loaded module class
    :param hbf_instance: hydrabus serial instance
    :return:
    """
    logger = Logger()
    ret, err = hbf_instance.current_module.check_args()
    if not ret:
        logger.print(err, "error")
    try:
        hbf_instance.current_module.run()
    except:
        logger.print("Error running module", "error")
        traceback.print_exc()
