from machine import Pin, UART
import time


class Uart:

    TX_PIN = 17
    RX_PIN = 16
    BAUDRATE = 9600
    MSG_SIZE = 21  # bytes
    SLEEP_MS = 50  # for busy loop

    def __init__(self):
        self.uart = UART(1, baudrate=self.BAUDRATE, tx=self.TX_PIN, rx=self.RX_PIN)

    def test_com(self):
        pass

    def get_state(self):
        data = ""
        while True:
            if self.uart.any():
                char = self.uart.read(1).decode()
                if char == "#":
                    break
                data += char
            else:
                time.sleep(self.SLEEP_MS / 1000)
        return data
    
