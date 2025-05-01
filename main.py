from communication import *
from traffic_light import *
from led_strip import *


# initializing objects
uart = Uart()
t_light_1 = TrafficLight([13, 14, 26, 25, 33, 32])
t_light_2 = TrafficLight([15, 2, 4, 5, 18, 19])
trafic_lights_modes = {
    0: "001100",
    1: "010010",
    2: "100001",
    3: "010010"
    }

led_strip = LedStrip(21, 23 * 4)

# testing objects
t_light_1.test_lights()
t_light_2.test_lights()
led_strip.test_led_strip()


# main code
while True:
    print("getting data...")
    data = uart.get_state()
    print("updating for the data:", data)
    if len(data) == 1:
        
        t_light_1.update(trafic_lights_modes[int(data)])
        t_light_2.update(trafic_lights_modes[int(data)])
    else:
        # replace the road's indexs to it whould be 0213 (like the physical roads) instead of 1234
        roads = data.split(".")
        roads[1], roads[2] = roads[2], roads[1]
        combined_road = ''.join(roads)
        print(type(combined_road), combined_road)
        led_strip.update(combined_road)
    
    
