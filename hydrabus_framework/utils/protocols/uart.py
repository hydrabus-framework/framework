from hydrabus_framework.utils.logger import Logger
from hydrabus_framework.utils.hb_generic_cmd import *


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


def hb_set_baudrate(serial_instance, baudrate):
    """
    Set the desired baudrate value to communicate with the target device.
    :param serial_instance: hydrabus serial instance
    :param baudrate: dictionnary containing desired baudrate speed in hexadecimal 'hex' and decimal 'dec' value
    :return: Bool
    """
    logger = Logger()
    hb_reset(serial_instance)
    if hb_init_uart(serial_instance):
        # Change baudrate speed
        serial_instance.write(baudrate["hex"])
        if b'\x01' != serial_instance.read(1):
            logger.handle("Failed to change baudrate", Logger.ERROR)
            return False
        logger.handle("Switching to baudrate: {}".format(baudrate["dec"]), Logger.SUCCESS)
        return True
    else:
        logger.handle("Failed to init BBIO_UART mode", Logger.ERROR)
        return False


def hb_switch_uart(serial_instance):
    """
    Switch hydrabus to UART mode
    :param serial_instance: hydrabus serial instance
    :return: Bool
    """
    logger = Logger()
    serial_instance.write(b'\x03')
    if "ART1".encode('utf-8') not in serial_instance.read(4):
        logger.handle("Cannot enter UART mode", Logger.ERROR)
        return False
    return True


def hb_init_uart(serial_instance):
    if hb_switch_bbio(serial_instance):
        if hb_switch_uart(serial_instance):
            return True
        return False
    return False
