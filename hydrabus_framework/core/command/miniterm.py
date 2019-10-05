import serial
import sys

from hydrabus_framework.utils.logger import Logger

from serial.tools.miniterm import Miniterm


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


def key_description(character):
    """
    generate a readable description for a key.
    :param character: an ascii character.
    :return: readable description for key.
    """
    ascii_code = ord(character)
    if ascii_code < 32:
        return 'Ctrl+{:c}'.format(ord('@') + ascii_code)
    else:
        return repr(character)


def miniterm(hbf_instance=None, config=None):
    """
    Run a serial console session (using miniterm from serial package).
    :param config: configparser instance.
    :param hbf_instance: Hydrabus framework instance (self).
    :return: Nothing.
    """
    logger = Logger()
    filters = []
    if hbf_instance is None and config is None:
        logger.handle("You need to set hbf_instance or config", logger.ERROR)
        return False
    if hbf_instance is not None:
        config = hbf_instance.config
    hydrabus_cfg = config['HYDRABUS']
    miniterm_cfg = config['MINITERM']
    filters.append(miniterm_cfg['filters'])

    while True:
        if hydrabus_cfg['port'] is None or hydrabus_cfg['port'] == '-':
            print('port is not given')
        try:
            serial_instance = serial.serial_for_url(
                hydrabus_cfg['port'],
                hydrabus_cfg['baudrate'],
                parity=miniterm_cfg['parity'],
                rtscts=None,
                xonxoff=config.getboolean('MINITERM', 'xonxoff'),
                do_not_open=True)

            if not hasattr(serial_instance, 'cancel_read'):
                # enable timeout for alive flag polling if cancel_read is not available
                serial_instance.timeout = 1

            if isinstance(serial_instance, serial.Serial):
                serial_instance.exclusive = True

            serial_instance.open()
        except serial.SerialException as e:
            logger.handle("could not open port {!r}: {}".format(hydrabus_cfg['port'], e), logger.ERROR)
            return False
        else:
            break

    miniterm = Miniterm(
        serial_instance,
        echo=config.getboolean('MINITERM', 'echo'),
        eol=miniterm_cfg['eol'].lower(),
        filters=filters)
    miniterm.exit_character = chr(int(miniterm_cfg['exit_char']))
    miniterm.menu_character = chr(int(miniterm_cfg['menu_char']))
    miniterm.raw = miniterm_cfg['raw']
    miniterm.set_rx_encoding(miniterm_cfg['serial_port_encoding'])
    miniterm.set_tx_encoding(miniterm_cfg['serial_port_encoding'])

    if not config.getboolean('MINITERM', 'quiet'):
        sys.stderr.write('--- Miniterm on {p.name}  {p.baudrate},{p.bytesize},{p.parity},{p.stopbits} ---\n'.format(
            p=miniterm.serial))
        sys.stderr.write('--- Quit: {} | Menu: {} | Help: {} followed by {} ---\n'.format(
            key_description(miniterm.exit_character),
            key_description(miniterm.menu_character),
            key_description(miniterm.menu_character),
            key_description('\x08')))

    miniterm.start()
    try:
        miniterm.join(True)
    except KeyboardInterrupt:
        pass
    if not config.getboolean('MINITERM', 'quiet'):
        sys.stderr.write('\n--- exit ---\n')
    miniterm.join()
    miniterm.close()
