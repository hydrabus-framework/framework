from hydrabus_framework.utils.logger import Logger
from hydrabus_framework.utils.hb_generic_cmd import hb_reset, hb_switch_bbio


__author__ = "Jordan Ovrè <ghecko78@gmail.com>"


def hb_switch_spi(serial_instance):
    """
    Switch hydrabus to SPI binary mode
    :param serial_instance: hydrabus serial instance
    :return: Bool
    """
    logger = Logger()
    serial_instance.write(b'\x01')
    if "SPI1".encode('utf-8') not in serial_instance.read(4):
        logger.handle("Cannot enter SPI binary mode", Logger.ERROR)
        return False
    return True


def hb_configure_spi_peripheral(serial_instance, config=None):
    """
    This function allows to select or unselect the SPI slave.
    None = unselect, 1 = select
    :param serial_instance: hydrabus serial instance
    :param config:
    :return:
    """
    logger = Logger()
    if config is None:
        serial_instance.write(0b01000000)
    if config == 1:
        serial_instance.write(0b01000001)
    else:
        logger.handle("Invalid value SPI config (valid value is None for unselect or 1 for select)", Logger.ERROR)


def hb_configure_spi_port(serial_instance, polarity="low", phase="low", spi_device="SPI1"):
    """
    Configure polarity, clock and spi device
    :param serial_instance: hydrabus serial instance
    :param polarity: clock polarity value (low or high)
    :param phase: clock phase value (low or high)
    :param spi_device: SPI device (SPI1 or SPI2)
    :return: Bool
    """
    base_cmd = 0b10000000
    logger = Logger()
    valid_device = {'SPI1': 0b00000001, 'SPI2': 0b00000000}
    valid_phase = {'low': 0b00000000, 'high': 0b00000010}
    valid_polarity = {'low': 0b00000000, 'high': 0b00000100}

    try:
        spi_device = valid_device.get(spi_device)
        phase = valid_phase.get(phase)
        polarity = valid_polarity.get(polarity)
        if spi_device is None:
            raise ValueError('Invalid SPI device selected (SPI1 or SP2)')
        if phase is None:
            raise ValueError('Invalid clock phase value (low or high)')
        if polarity is None:
            raise ValueError('Invalid clock polarity value (low or high)')
    except ValueError as err:
        logger.handle(err, Logger.ERROR)
        return False

    config = base_cmd + spi_device + phase + polarity
    serial_instance.write(bytes([config]))
    if b'\x01' != serial_instance.read(1):
        logger.handle("Cannot set SPI device settings, try again or reset hydrabus. ", Logger.ERROR)
        return False
    return True


def set_spi_speed(serial_instance, spi_speed, spi_device="SPI1"):
    """
    Configure the spi speed
    :param serial_instance: hydrabus serial instance
    :param spi_speed: string speed
    :param spi_device: the configured SPI device
    :return: Bool
    0b01100xxx
    """
    logger = Logger()
    base_cmd = 0b01100000
    valid_spi1_speed = {'320KHZ': 0b000, '650KHZ': 0b001, '1.31MHZ': 0b010, '2.62MHZ': 0b011,
                        '5.25MHZ': 0b100, '10.5MHZ': 0b101, '21MHZ': 0b110, '42MHZ': 0b111}
    valid_spi2_speed = {'160KHZ': 0b000, '320KHZ': 0b001, '650KHZ': 0b010, '1.31MHZ': 0b011,
                        '2.62MHZ': 0b100, '5.25MHZ': 0b101, '10.5MHZ': 0b110, '21MHZ': 0b111}
    if spi_device.upper() == "SPI1":
        for string_speed, bin_speed in valid_spi1_speed.items():
            if string_speed == spi_speed.upper():
                speed = base_cmd + bin_speed
                serial_instance.write(bytes([speed]))
                if b'\x01' not in serial_instance.read(1):
                    logger.handle("Cannot set SPI speed, try again or reset hydrabus.", Logger.ERROR)
                    return False
                return True
        else:
            logger.handle("Invalid spi speed", Logger.ERROR)
            return False
    elif spi_device.upper() == "SPI2":
        for string_speed, bin_speed in valid_spi2_speed.items():
            if string_speed == spi_speed.upper():
                speed = base_cmd + bin_speed
                serial_instance.write(bytes([speed]))
                if b'\x01' not in serial_instance.read(1):
                    logger.handle("Cannot set SPI speed, try again or reset hydrabus.", Logger.ERROR)
                    return False
                return True
        else:
            logger.handle("Invalid spi speed", Logger.ERROR)
            return False
    else:
        logger.handle("Invalid spi device", Logger.ERROR)
        return False
