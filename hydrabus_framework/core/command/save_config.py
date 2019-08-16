from pathlib import Path


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


def save_config(hbf_instance):
    """
    Save the current config into hbf.cfg file
    :param hbf_instance: Hydrabus framework instance (self)
    :return: Nothing
    """
    hbf_config_path = Path.home() / '.hbf' / 'hbf.cfg'
    with hbf_config_path.open('w') as cfg_file:
        hbf_instance.config.write(cfg_file)
