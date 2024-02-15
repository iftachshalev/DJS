from road import *


class Junction:

    ROADS = [2.3, 2.5, 4.1, 4.5, 6.1, 6.3]
    COMBINATIONS = [[6.3, 6.1, 4.5], [2.3, 2.5, 4.5], [2.3, 4.1, 4.5]]

    def __init__(self, detailed_print=False):
        self.roads = [Road(i) for i in self.ROADS]
        self.green_comb = self.COMBINATIONS[0]
        self.green_time = 0
        self.time_sec = 0
        self.detailed_print = detailed_print

    def advance_junction(self, sec):
        for i in self.roads:
            if i.road_name in self.green_comb:
                i.advance_green_road(sec)
            else:
                i.advance_red_road(sec)
        self.time_sec += sec

    def action_algo(self):
        pass

    def __repr__(self):
        s = ""
        for i in self.roads:
            if self.detailed_print:
                s += f"ROAD {i.road_name}: there are {len(i.cars)} cars and {len(i.passed)} passed\n"
                s += i.__repr__()
            else:
                s += f"ROAD {i.road_name}: there are {len(i.cars)} cars and {len(i.passed)} passed\n"
        s += f"time since init: {self.time_sec}\n"
        return s
