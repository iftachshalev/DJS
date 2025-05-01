import time
import serial
from itertools import accumulate

connected = False

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

    data: "road1.road2.road3.road4.traffic lights cycle"

    """

    NUM_LEDS_IN_ROAD = 23
    ROAD_LENGTH_IN_SIM = 124  # [m]  -- needs to be updated with every change

    def __init__(self):
        """
        self.cycle = [(False, True), (False, False), (True, False), (False, False)]
        self.roads = [[0, 2], [1, 3]]  # WEST, EAST, SOUTH NORTH
        self.lights_str = {
            0: "001100.001100",
            1: "010010.010010",
            2: "100001.100001",
            3: "010010.010010"
        }
        """
        if connected:
            self.ser = serial.Serial('/dev/ttyAMA0', 9600)
        self.current_cycle = None
        self.led_strips = ["0" * self.NUM_LEDS_IN_ROAD for i in range(4)]



    def send_cycle(self):
        data = str(self.current_cycle) + "#"
        if connected:
            self.ser.write(data.encode())
        print("sending cycle:", data)

    def send_vehicles(self):
        data = ".".join(self.led_strips) + "#"
        if connected:
            self.ser.write(data.encode())
        print("sending leds:", data)

    def update_cycle(self, cycle):
        self.current_cycle = cycle

    def update_cars(self, roads, _print=False):
        converted_roads = self.convert_roads(roads)

        self.led_strips = []  # reset LED strips

        for i, car_positions in enumerate(converted_roads):
            # Initialize count per LED
            led_counts = [0] * self.NUM_LEDS_IN_ROAD

            for x in car_positions:
                # Clamp x to [0, self.ROAD_LENGTH_IN_SIM]
                x = max(0, min(x, self.ROAD_LENGTH_IN_SIM))

                # Map position x to an LED index
                index = int((x / self.ROAD_LENGTH_IN_SIM) * (self.NUM_LEDS_IN_ROAD - 1))
                led_counts[index] += 1

            # Turn the counts into a string (convert numbers to strings)
            led_string = ''.join(str(min(count, 9)) for count in led_counts)  # cap at 9 to avoid double-digit chars

            self.led_strips.append(led_string)

            if _print:
                print(f"LED Strip {i}: {led_string}")


    @staticmethod
    def convert_roads(roads):
        """
        returns the `converted_roads` attribute by combining vehicle positions from multiple road segments.

        Each road in `converted_roads` is formed by merging vehicle positions from a predefined set of road segments.
        The positions are adjusted by adding an offset (`boost`), which represents the cumulative length of the
        preceding road segments.

        Args:
            roads (list): A list of road objects, where each road contains at least:
                - `length` (int): The length of the road.
                - `vehicles` (list): A list of vehicle objects, where each vehicle has an attribute `x` representing its position.

        Road Combinations:
            0: Roads [0, 8, 6]
            1: Roads [1, 9, 7]
            2: Roads [2, 10, 4]
            3: Roads [3, 11, 5]

        Updates:
            - `converted_roads[i]` is updated with the adjusted vehicle positions for each combined road.
            - The positions of vehicles are calculated relative to the start of the combined road.

        Example:
            Suppose `roads[0]` has vehicles at [10, 20], `roads[8]` at [5, 15], and `roads[6]` at [0, 8],
            with respective lengths 100 and 50.
            Then, `self.roads[0]` will store: [10, 20, 105, 115, 150, 158]
        """
        roads_definitions = [[0, 8, 6], [1, 9, 7], [2, 10, 4], [3, 11, 5]]
        converted_roads = [[], [], [], []]  # lists of x's of every in-bound car in combined roads 0 -> 3

        for i, semmy_roads in enumerate(roads_definitions):
            # Fetch road objects corresponding to the indices in semmy_roads
            road_objects = [roads[idx] for idx in semmy_roads]

            # Compute the offsets (boosts) based on cumulative road lengths
            boosts = list(accumulate([0] + [r.length for r in road_objects[:-1]]))

            # Collect and adjust vehicle positions
            cars_dis = []
            for boost, road in zip(boosts, road_objects):
                cars_dis.extend([z.x + boost for z in road.vehicles])

            # Update the corresponding road in self.roads
            converted_roads[i] = cars_dis

        return converted_roads


