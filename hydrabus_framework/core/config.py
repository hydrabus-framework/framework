import configparser

from pathlib import Path


def create_default_config(config, hbf_dir, hbf_config_path):
    """
    :param config: configparser instance
    :param hbf_dir: pathlib object of the home directory of the current user
    :param hbf_config_path: pathlib object of the configuration path located in the home's current user
    :return: Nothing
    """
    if not hbf_dir.is_dir():
        hbf_dir.mkdir()
    config['HYDRABUS'] = {
        'port': '/dev/ttyACM0',
        'baudrate': '115200',
        'read_timeout': 1
    }
    config['MINITERM'] = {
        'parity': 'N',
        'xonxoff': False,
        'echo': False,
        'filters': 'default',
        'raw': False,
        'quiet': False,
        'exit_char': 0x1d,
        'menu_char': 0x14,
        'serial_port_encoding': 'UTF-8',
        'eol': 'CR'
    }
    with hbf_config_path.open('w') as cfg_file:
        config.write(cfg_file)


def load_config():
    config = configparser.ConfigParser(allow_no_value=True)
    hbf_dir = Path.home() / '.hbf'
    hbf_config_path = hbf_dir / 'hbf.cfg'
    if not hbf_dir.is_dir() or not hbf_config_path.is_file():
        create_default_config(config, hbf_dir, hbf_config_path)
    config.read(str(hbf_config_path))
    return config
