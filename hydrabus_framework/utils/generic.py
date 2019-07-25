import time


def reset_hb(hb_instance):
    """
    Reset hydrabus to return in console mode
    :param hb_instance: hydrabus serial instance
    """
    hb_instance.write(b'\x00')
    hb_instance.write(b'\x0F')
    time.sleep(0.2)
    # clean serial buffer
    hb_instance.read(hb_instance.in_waiting)


def close_hb(hb_instance):
    """
    Close hydrabus serial instance
    :param hb_instance: hydrabus serial instance
    """
    hb_instance.close()


def init_bbio(hb_instance):
    """
    Init the hydrabus to switch into BBIO mode
    :param hb_instance: hydrabus serial instance
    :return: Bool
    """
    for i in range(20):
        hb_instance.write(b'\x00')
    if "BBIO1".encode('utf-8') not in hb_instance.read(5):
        return False
    return True
