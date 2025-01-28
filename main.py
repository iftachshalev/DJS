from communication import *
from traffic_light import *
from led_strip import *


# initializing objects
uart = Uart()
"""t_light_1 = TrafficLight([13, 12, 14, 27, 26, 25])
t_light_2 = TrafficLight([15, 2, 4, 5, 18, 19])
led1 = ()
led2 = LedStrip()
led3 = LedStrip()
led4 = LedStrip()"""
objects = [LedStrip(), LedStrip(), LedStrip(), LedStrip(),
           TrafficLight([13, 12, 14, 27, 26, 25]), TrafficLight([15, 2, 4, 5, 18, 19])
           ]  # if we are using the array instead of individuals than the order needs to be the same as in data bellow

while True:
    data = uart.get_state().split(".")  # ["0010", "1110", "1011", "1000", "000110", "110111"] first 4 are leds, last 2 are tls
    for i, value in enumerate(data):
        objects[i].update(value)
