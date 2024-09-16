from road import Road
from action import ActionDecider


class Junction:

    # junction depending
    ROADS = [1.2, 1.3, 2.1, 3.1, 3.2]  # Enter.Exit
    COMBINATIONS = [[1.2, 2.1], [3.1, 3.2], [1.3, 1.2]]

    SWITCH_PENALTY = 1  # [s] unrealistic
    CAMERA_DISTANCE = 50  # [m]
    NUM_CARS = 5  # format should be changed to allow different number of cars between roads

    def __init__(self, detailed_print=False):

        # initializing each road with cars in a {num: road_object} dict
        self.roads = {}
        for i in self.ROADS:
            self.roads[i] = Road(self.NUM_CARS)

        # initializing some junction params
        self.green_comb = self.COMBINATIONS[0]
        self.green_time = 0
        self.time_sec = 0
        self.detailed_print = detailed_print
        self.next_green_comb = self.COMBINATIONS[0]
        self.switched = 0
        self.tick_count = 0
        self.snapshot = self.init_snapshot()
        print_mat(self.snapshot)

        # initializing action model? figure this out
        self.action_decider = ActionDecider(self.COMBINATIONS)

        print(self.start_of_simulation())

    def run(self, tick=0.1):

        # update lights and advance JC -> check if ended -> if not, get the next light that need to be green and repeat
        while True:
            self.advance_junction(tick)
            print(self.__repr__())

            if self.is_ended():
                print(self.end_of_simulation())
                break

            self.get_action()

    def update_green_comb(self):
        if self.next_green_comb != self.green_comb:
            self.green_comb = self.next_green_comb
            self.green_time = 0
            self.switched += 1
            self.time_sec += self.SWITCH_PENALTY  # should cars advance?

    def advance_junction(self, tick):

        # update lights
        self.update_green_comb()

        # advancing red and green roads
        for i in list(self.roads.keys()):
            if i in self.green_comb:
                self.roads[i].advance_green_road(tick)

            else:
                self.roads[i].advance_red_road(tick)
        self.time_sec += tick
        self.green_time += tick

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

    def init_snapshot(self):

        # finding the number of ways in the junction using the provided roads
        ways = max([int(str(i).split(".")[0]) for i in self.ROADS]+[int(str(i).split(".")[1]) for i in self.ROADS])

        snap = []
        for i in range(1, ways + 1):
            snap.append([])
            for j in range(1, ways + 1):
                if float(f"{i}.{j}") in self.ROADS:
                    val = [0]

                    # adding the index of the combs to each road in the snap
                    for k in range(len(self.COMBINATIONS)):
                        if float(f"{i}.{j}") in self.COMBINATIONS[k]:
                            val.append(k)
                    snap[i - 1].append(val)
                else:
                    snap[i-1].append(None)
        return snap

    def update_snapshot(self):
        for i in self.ROADS:
            enter = int(str(i).split(".")[0])
            exit_ = int(str(i).split(".")[1])
            self.snapshot[enter-1][exit_-1][0] = len(self.roads[i].cars)

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

    def start_of_simulation(self):
        return f"starting simulation...\n\n starting point:\n{self.__repr__()}"

    def end_of_simulation(self):
        return (f"***ENDED ON TIME: {self.time_sec}***\n"
                f"\t>>>total cars that passed:        |  {sum([len(j.passed) for j in self.roads.values()])}\n"
                f"\t>>>total cars that didn't pass:   |  {sum([len(j.cars) for j in self.roads.values()])}\n"
                f"\t>>>total switches:                |  {self.switched}\n")


def print_mat(mat):
    s = [[str(e) for e in row] for row in mat]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))

