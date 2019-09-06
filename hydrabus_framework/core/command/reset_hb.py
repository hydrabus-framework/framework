import serial

from hydrabus_framework.utils.logger import Logger
from hydrabus_framework.utils.hb_generic_cmd import hb_reset, hb_close, hb_connect


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


def reset_hb(hbf_instance):
    """
    Return hydrabus into console mode
    :param hbf_instance: Hydrabus framework instance (self)
    :return: Nothing
    """
    logger = Logger()
    hydrabus_cfg = hbf_instance.config['HYDRABUS']
    if hydrabus_cfg['port'] is None or hydrabus_cfg['port'] == '-':
        logger.handle('port is not set on the configuration (setc command)', Logger.ERROR)
    else:
        try:
            serial_instance = hb_connect(device=hydrabus_cfg['port'], baudrate=115200, timeout=1)
        except serial.SerialException as e:
            logger.handle("could not open port {!r}: {}".format(hydrabus_cfg['port'], e), logger.ERROR)
            return
        except UserWarning as err:
            logger.handle("{}".format(err), Logger.ERROR)
            return
        hb_reset(serial_instance)
        hb_close(serial_instance)
        logger.handle("Reset sequence successfully sent to Hydrabus...", Logger.SUCCESS)
