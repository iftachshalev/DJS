from machine import Pin, UART
import time


class Uart:

    TX_PIN = 17
    RX_PIN = 16
    BAUDRATE = 9600

    def __init__(self):
        self.uart = UART(1, baudrate=BAUDRATE, tx=TX_PIN, rx=RX_PIN, timeout=None)

    def test_com(self):
        pass

    def get_state(self):
        data = decode(self.uart.read())
        return data


