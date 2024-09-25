from road import Road
from action import ActionDecider
from config_handler import *
import logging as log

log.basicConfig(level=log.DEBUG,
                    format='%(levelname)s - %(message)s',
                    filename='app.log',
                    filemode='w')
class Junction:

    def __init__(self, detailed_print=False):
        self.detailed_print = detailed_print

        # initializing each road with cars in a {num: road_object} dict
        self.roads = {}
        for i in CONF.ROADS:
            self.roads[i] = Road(CONF.NUM_CARS, CONF.MAX_VEHICLE_DISTANCE)

        # initializing some junction params
        self.green_comb = 0  # the index of the activated combination in the combs array in the config
        self.green_time = 0  # [s] the time that the current combination has been active
        self.sim_time = 0  # [s] the calculated total time of the simulation
        self.switched = 0  # the amount of times the lights switched
        self.snapshot = self.init_snapshot()  # snapshot of the junction as a matrix for the RL model
        self.update_snapshot()

        # initializing action model? figure this out
        self.action_decider = ActionDecider(CONF.COMBINATIONS)

    def run(self, tick=0.1):

        """
        need:
            1. get action
            2. update the junction according to the action
            3. advance the junction 1 tick
            4. print info
            5. repeat

        to do:
            self.get_action return the action instead of changing self.next_green_comb for clean code -- DONE
        """

        print(self.start_of_simulation())  # printing the starting info

        while True:
            self.update_snapshot()  # the action decider is using the snap, so we need to update it
            action = self.get_action()  # - 1

            if action != self.green_comb:
                self.update_green_comb(action)  # - 2 - a lot of problem with the switching - figur this out

            print("advancing....\n")
            self.advance_junction(tick)  # - 3
            self.sim_time += tick
            self.green_time += tick

            self.print_state()  # - 4

            if self.is_ended():
                print(self.end_of_simulation())
                break

    def update_green_comb(self, action):
        print(f"witching: {CONF.COMBINATIONS[self.green_comb]} ---> {CONF.COMBINATIONS[action]}")
        self.green_comb = action
        self.green_time = 0
        self.switched += 1
        self.sim_time += CONF.SWITCH_PENALTY  # should cars advance? <<<<<<<======

    def advance_junction(self, tick):

        for i in CONF.ROADS:
            if i in CONF.COMBINATIONS[self.green_comb]:
                self.roads[i].advance_green_road(tick, self.green_time)  # ======>>>>> check for consistency in GT

            else:
                self.roads[i].advance_red_road(tick)

    def get_action(self):
        return self.action_decider.most_cars(self.snapshot, self.green_comb, self.green_time)

    def is_ended(self):
        for i in self.roads.values():
            if len(i.cars) != 0:
                return False
        return True

    @staticmethod
    def init_snapshot():

        # finding the number of ways in the junction using the provided roads
        ways = max([int(str(i).split(".")[0]) for i in CONF.ROADS]+[int(str(i).split(".")[1]) for i in CONF.ROADS])

        snap = []
        for i in range(1, ways + 1):
            snap.append([])
            for j in range(1, ways + 1):
                if float(f"{i}.{j}") in CONF.ROADS:
                    val = [0]

                    # adding the index of the combs to each road in the snap
                    for k in range(len(CONF.COMBINATIONS)):
                        if float(f"{i}.{j}") in CONF.COMBINATIONS[k]:
                            val.append(k)
                    snap[i - 1].append(val)
                else:
                    snap[i-1].append(None)
        return snap

    def update_snapshot(self):  # need to take into account the camera distance value
        for i in CONF.ROADS:
            cars_in_dis = 0
            for j in self.roads[i].cars:
                if j.distance < CONF.CAMERA_DISTANCE:
                    cars_in_dis += 1

            enter = int(str(i).split(".")[0])
            exit_ = int(str(i).split(".")[1])
            self.snapshot[enter-1][exit_-1][0] = cars_in_dis

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
        s += f"time since init: {self.sim_time}\ngreen comb {CONF.COMBINATIONS[self.green_comb]}\n\n"
        s += f"the junction snapshot: \n{nice_mat(self.snapshot)}\n\n\n"
        return s

    def print_state(self):

        meter_char_sign = 10  # cannot be 0

        print(f"after {self.sim_time} seconds, this is the state:")
        print(f"green combination: {CONF.COMBINATIONS[self.green_comb]} for {self.green_time} seconds")

        for i in CONF.ROADS:

            if i in CONF.COMBINATIONS[self.green_comb]:
                print(f"{bcolors.OKGREEN}ROAD {i}: {bcolors.ENDC}", end="")
            else:
                print(f"{bcolors.FAIL}ROAD {i}: {bcolors.ENDC}", end="")

            road_str = "-"*(int(CONF.MAX_VEHICLE_DISTANCE/meter_char_sign) + 1)  # +1 for no index out of range

            for j in self.roads[i].cars:
                place_idx = int(j.distance/meter_char_sign)

                if place_idx < 5:
                    log.debug((j.distance, int(j.distance/meter_char_sign)))

                if road_str[place_idx] == "-":
                    road_str = road_str[:place_idx] + "1" + road_str[place_idx+1:]
                else:
                    road_str = road_str[:place_idx] + str(int(road_str[place_idx]) + 1) + road_str[place_idx + 1:]

            if CONF.CAMERA_DISTANCE >= CONF.MAX_VEHICLE_DISTANCE:
                pass
            else:
                camera_idx = int(CONF.CAMERA_DISTANCE/meter_char_sign)  # accurate print - it should be divisible
                road_str = road_str[:camera_idx] + f"{bcolors.ENDC}" + road_str[camera_idx:]

            road_str = f"{bcolors.OKBLUE}{road_str}|==> {len(self.roads[i].cars)} cars"

            print(road_str)
        self.update_snapshot()
        print(nice_mat(self.snapshot))

        print("\n\n\n")

    def start_of_simulation(self):
        return f"starting point:\n{self.__repr__()}"

    def end_of_simulation(self):
        return (f"***ENDED ON TIME: {self.sim_time}***\n"
                f"\t>>>total cars that passed:        |  {sum([len(j.passed) for j in self.roads.values()])}\n"
                f"\t>>>total cars that didn't pass:   |  {sum([len(j.cars) for j in self.roads.values()])}\n"
                f"\t>>>total switches:                |  {self.switched}\n")


def nice_mat(mat):
    s = [[str(e) for e in row] for row in mat]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    return '\n'.join(table)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'