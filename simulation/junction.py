from road import Road
from action import ActionDecider


class Junction:

    ROADS = [2.3, 2.5, 4.1, 4.5, 6.1, 6.3]
    COMBINATIONS = [[6.3, 6.1, 4.5], [2.3, 2.5, 4.5], [2.3, 4.1, 4.5]]
    SWITCH_PENALTY_SEC = 1  # unrealistic

    def __init__(self, detailed_print=False):
        self.roads = [Road(i, 1000) for i in self.ROADS]
        self.green_comb = self.COMBINATIONS[0]
        self.green_time = 0
        self.time_sec = 0
        self.detailed_print = detailed_print
        self.action_decider = ActionDecider(self.COMBINATIONS)
        self.next_green_comb = self.COMBINATIONS[0]
        self.switched = 0

    def update_green_comb(self):
        if self.next_green_comb != self.green_comb:
            self.time_sec += self.SWITCH_PENALTY_SEC
            self.green_comb = self.next_green_comb
            self.green_time = 0
            self.switched += 1

    def advance_junction(self, sec):

        self.update_green_comb()

        for i in self.roads:
            if i.road_name in self.green_comb:
                i.advance_green_road(sec)

            else:
                i.advance_red_road(sec)
        self.time_sec += sec
        self.green_time += sec

    def action_algo(self):
        road_cars_dict = {}
        for i in self.roads:
            road_cars_dict[i.road_name] = len(i.cars)

        self.next_green_comb = self.action_decider.most_cars(road_cars_dict, self.green_comb, self.green_time)

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

    def end_of_simulation(self):
        return (f"***ENDED ON TIME: {self.time_sec}***\n"
                f"\t>>>total cars that passed:        |  {sum([len(j.passed) for j in self.roads])}\n"
                f"\t>>>total cars that didn't pass:   |  {sum([len(j.cars) for j in self.roads])}\n"
                f"\t>>>total switches:                |  {self.switched}\n")
