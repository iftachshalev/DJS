import serial
import time


class Communication:

    """
    this works with the assumption that we are using the two_way_intersection.py file as the junction setup, since
    the physical simulation is fixed.


      N


    |-------|
    |       |  "NrNyNgErEyEg"
    | 1     |
    |-------|

    |-------|
    |       |  "SrSySgWrWyWg"
    | 2     |
    |-------|


      S

    """
    def __init__(self):
        self.cycle = [(False, True), (False, False), (True, False), (False, False)]
        self.roads = [[0, 2], [1, 3]]  # WEST, EAST, SOUTH NORTH
        self.lights_str = {
            0: "001100.001100",
            1: "010010.010010",
            2: "100001.100001",
            3: "010010.010010"
        }
        self.current_cycle = None
        self.ser = serial.Serial('/dev/ttyAMA0', 9600)

    def send_data(self):
        data = "0.0.0.0." + self.lights_str[self.current_cycle]
        self.ser.write(data.encode())
        print("sending:", data)

    def update_cycle(self, cycle):
        self.current_cycle = cycle
        self.send_data()
