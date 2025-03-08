# import serial
import time
from itertools import accumulate


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
        # self.ser = serial.Serial('/dev/ttyAMA0', 9600)
        self.roads = [[], [], [], []]  # lists of x's of every in-bound car in combined roads 0 -> 3
        self.num_leds_in_road = 30

    def send_data(self):
        data = "0.0.0.0." + self.lights_str[self.current_cycle]
        # self.ser.write(data.encode())
        print("sending:", data)

    def update_cycle(self, cycle):
        self.current_cycle = cycle

    def update_cars(self, roads, _print=False):
        """
        Updates the `self.roads` attribute by combining vehicle positions from multiple road segments.

        Each road in `self.roads` is formed by merging vehicle positions from a predefined set of road segments.
        The positions are adjusted by adding an offset (`boost`), which represents the cumulative length of the
        preceding road segments.

        Args:
            roads (list): A list of road objects, where each road contains at least:
                - `length` (int): The length of the road.
                - `vehicles` (list): A list of vehicle objects, where each vehicle has an attribute `x` representing its position.
            _print (bool, optional): If True, prints the updated roads and vehicle positions. Default is False.

        Road Combinations:
            0: Roads [0, 8, 6]
            1: Roads [1, 9, 7]
            2: Roads [2, 10, 4]
            3: Roads [3, 11, 5]

        Updates:
            - `self.roads[i]` is updated with the adjusted vehicle positions for each combined road.
            - The positions of vehicles are calculated relative to the start of the combined road.

        Example:
            Suppose `roads[0]` has vehicles at [10, 20], `roads[8]` at [5, 15], and `roads[6]` at [0, 8],
            with respective lengths 100 and 50.
            Then, `self.roads[0]` will store: [10, 20, 105, 115, 150, 158]
        """
        roads_definitions = [[0, 8, 6], [1, 9, 7], [2, 10, 4], [3, 11, 5]]

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
            self.roads[i] = cars_dis

        if _print:
            for i, road in enumerate(self.roads):
                print(f"road {i}: {road}")


