import machine
import neopixel
import time


class LedStrip:

    def __init__(self, led_strip_pin, num_leds):
        self.num_leds = num_leds
        self.np = neopixel.NeoPixel(machine.Pin(led_strip_pin), self.num_leds)

    def test_led_strip(self):
        for i in range(self.num_leds):
            self.np.fill((0, 0, 0))       # Turn all LEDs off
            self.np[i] = (0, 0, 255)      # Light current LED green
            self.np.write()
            time.sleep(0.1)

        for i in range(3):
            self.np.fill((0, 255, 0))
            self.np.write()
            time.sleep(0.8)

            self.np.fill((0, 0, 0))
            self.np.write()
            time.sleep(0.2)

    def update(self, new_state):  # new state - "01001001"
        for i, bit in enumerate(new_state):
            if bit == '1':
                self.np[i] = (255, 255, 255)  # White light, can change to any RGB
            elif bit == '0':
                self.np[i] = (0, 0, 0)        # LED off
            else:
                self.np[i] = (255, 0, 0)
        self.np.write()

