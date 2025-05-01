from machine import Pin
import time


class TrafficLight:

    def __init__(self, pins):  # pins - [r, y, g, r, y, g] first 3 are front leds other 3 are side leds
        self.lights = [Pin(i, Pin.OUT) for i in pins]  # Pin moduls for the whole TL

    def test_lights(self):
        for i in range(6):
            s = "000000"
            s = s[:i] + "1" + s[i + 1:]
            self.update(s)
            time.sleep(0.2)
        for i in range(3):
            self.update("111111")
            time.sleep(0.4)
            self.update("000000")
            time.sleep(0.1)

    def update(self, new_state):  # new_state = "001010" according to the new state
        for i, char in enumerate(new_state):
            self.lights[i].value(int(char))

