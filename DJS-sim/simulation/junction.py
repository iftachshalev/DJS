from road import Road
from action import ActionDecider


class Junction:

    ROADS = [2.3, 2.5, 4.1, 4.5, 6.1, 6.3]
    COMBINATIONS = [[6.3, 6.1, 4.5], [2.3, 2.5, 4.5], [2.3, 4.1, 4.5]]
    SWITCH_PENALTY_SEC = 1  # unrealistic
    CAMERA_DISTANCE = 50  # [m]
    NUM_CARS = 5  # format should be changed to allow different number of cars between roads

    def __init__(self, detailed_print=False):
        self.roads = {}
        for i in self.ROADS:
            self.roads[i] = Road(self.NUM_CARS)
        self.green_comb = self.COMBINATIONS[0]
        self.green_time = 0
        self.time_sec = 0
        self.detailed_print = detailed_print
        self.action_decider = ActionDecider(self.COMBINATIONS)
        self.next_green_comb = self.COMBINATIONS[0]
        self.switched = 0
        self.tick_count = 0

    def run(self, tick=0.1):

        while True:
            self.advance_junction(tick)
            print(self.__repr__())

            if self.is_ended():
                print(self.end_of_simulation())
                break

            self.get_action()

    def update_green_comb(self):
        if self.next_green_comb != self.green_comb:
            self.time_sec += self.SWITCH_PENALTY_SEC
            self.green_comb = self.next_green_comb
            self.green_time = 0
            self.switched += 1

    def advance_junction(self, sec):

        self.update_green_comb()

        for i in list(self.roads.keys()):
            if i in self.green_comb:
                self.roads[i].advance_green_road(sec)

            else:
                self.roads[i].advance_red_road(sec)
        self.time_sec += sec
        self.green_time += sec

    @staticmethod
    def get_cars_in_distance(cars, dist):
        sum_of_cars = 0
        for i in cars:
            if i.distance <= dist:
                sum_of_cars += 1
        return sum_of_cars

    def get_comb_cars(self):
        comb_cars = []
        for i in self.COMBINATIONS:
            temp = []
            for j in i:
                temp.append(self.get_cars_in_distance(self.roads[j].cars, self.CAMERA_DISTANCE))
            comb_cars.append(sum(temp))
        return comb_cars

    def get_action(self):

        comb_cars = self.get_comb_cars()
        self.next_green_comb = self.action_decider.most_cars(comb_cars, self.green_comb, self.green_time)

    def is_ended(self):
        for i in self.roads.values():
            if len(i.cars) != 0:
                return False
        return True

    def __repr__(self):
        s = ""
        for i in self.roads.values():
            if self.detailed_print:
                s += (f"ROAD {list(self.roads.keys())[list(self.roads.values()).index(i)]}: there are {len(i.cars)} "
                      f"cars and {len(i.passed)} passed\n")
                s += i.__repr__()
            else:
                s += (f"ROAD {list(self.roads.keys())[list(self.roads.values()).index(i)]}: there are {len(i.cars)} "
                      f"cars and {len(i.passed)} passed\n")
        s += f"time since init: {self.time_sec}\ngreen comb {self.green_comb}\n\n"
        return s

    def end_of_simulation(self):
        return (f"***ENDED ON TIME: {self.time_sec}***\n"
                f"\t>>>total cars that passed:        |  {sum([len(j.passed) for j in self.roads.values()])}\n"
                f"\t>>>total cars that didn't pass:   |  {sum([len(j.cars) for j in self.roads.values()])}\n"
                f"\t>>>total switches:                |  {self.switched}\n")
