from machine import Pin


class TrafficLight:

    def __init__(self, pins):  # pins - [r, y, g, r, y, g] first 3 are front leds other 3 are side leds
        self.lights = [Pin(i, Pin.OUT) for i in pins]  # Pin moduls for the whole TL

    def test_lights(self):
        pass

    def update(self, new_state):  # new_state = "001010" according to the new state
        for i, char in enumerate(new_state):
            self.lights[i].value = int(char)

