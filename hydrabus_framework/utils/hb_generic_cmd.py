import time
import serial
from hydrabus_framework.utils.logger import Logger


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


def hb_reset(serial_instance):
    """
    Reset hydrabus to return in console mode
    :param serial_instance: hydrabus serial instance
    """
    serial_instance.write(b'\x00')
    serial_instance.write(b'\x0F')
    time.sleep(0.2)
    # clean serial buffer
    serial_instance.read(serial_instance.in_waiting)


def hb_close(serial_instance):
    """
    Close hydrabus serial instance
    :param serial_instance: hydrabus serial instance
    """
    serial_instance.close()


def hb_switch_bbio(serial_instance):
    """
    Init the hydrabus to switch into BBIO mode
    :param serial_instance: hydrabus serial instance
    :return: Bool
    """
    for i in range(20):
        serial_instance.write(b'\x00')
    if "BBIO1".encode('utf-8') not in serial_instance.read(5):
        return False
    return True


def hb_wait_ubtn(serial_instance):
    """
    Loop until user press hydrabus UBTN
    :param serial_instance: hydrabus serial instance
    :return: Nothing
    """
    # timeout=1 minutes
    timeout = time.time() + 60 * 1
    while True:
        if serial_instance.read(1) == 'B'.encode('utf-8'):
            if serial_instance.read(3) == 'BIO'.encode('utf-8'):
                # carriage return needed to reset interface
                serial_instance.write(b'\x0D\x0A')
                time.sleep(0.2)
                serial_instance.read(serial_instance.in_waiting)
                break
        if time.time() > timeout:
            logger = Logger()
            logger.handle("Wait UBTN timeout reached", Logger.ERROR)
            break


def hb_connect(device, baudrate, timeout):
    """
    Connect to the hydrabus device
    :param device: String, hydrabus device path
    :param baudrate: integer, baudrate speed to communicate with hydrabus
    :param timeout: integer, read timeout value (sec)
    :return: serial instance
    """
    logger = Logger()
    try:
        serial_instance = serial.Serial(device, baudrate, timeout=timeout)
        return serial_instance
    except serial.serialutil.SerialException as err:
        logger.handle(err, Logger.ERROR)
        return False
