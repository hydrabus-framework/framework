from core.logger import Logger


def run_module(hbf_instance):
    """
    Check all arguments and run the selected module
    :param current_module: Class, Current loaded module class
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
