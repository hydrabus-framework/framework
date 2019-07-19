import serial


class HBSerial:
    def __init__(self, config):
        self.device = config["hb_serial"]["Device"]
        self.baudrate = config["hb_serial"]["Baudrate"]
        self.hb_session = serial.Serial(self.device, self.baudrate)
        print("init")

    def is_open(self):
        print("check if serial open")
        if self.hb_session.is_open:
            return True
        else:
            return False

    def connect(self):
        print("connect")
        self.hb_session.open()

    def read(self):
        print("read")

    def write(self, data):
        print("write")

    def close(self):
        print("disconnect")
        self.hb_session.close()

    def interact(self):
        if self.is_open():
            print("interact, prompt with key binding, loop read write")
        else:
            print("return error and message")
