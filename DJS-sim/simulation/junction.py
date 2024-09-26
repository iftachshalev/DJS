from road import Road
from action import ActionDecider
from config_handler import *
from output_log import Output


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

        # init the output module
        self.output = Output()

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

        self.output.start_of_simulation(self)  # printing the starting info

        while True:
            self.update_snapshot()  # the action decider is using the snap, so we need to update it
            action = self.get_action()  # - 1

            if action != self.green_comb:
                self.output.print_str(f"witching: {CONF.COMBINATIONS[self.green_comb]} ---> {CONF.COMBINATIONS[action]}")
                self.switch_comb(action)  # - 2 - a lot of problem with the switching - figur this out

            self.output.print_str(f"advancing {tick} seconds\n")
            self.advance_junction(tick)  # - 3
            self.sim_time += tick
            self.green_time += tick

            self.output.print_state(self)  # - 4

            if self.is_ended():
                self.output.end_of_simulation(self)
                break

    def get_action(self):
        return self.action_decider.most_cars(self.snapshot, self.green_comb, self.green_time)  # <== inputs for RL model

    def switch_comb(self, action):
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

    def is_ended(self):
        for i in self.roads.values():
            if len(i.cars) != 0:
                return False
        return True

    @staticmethod
    def init_snapshot():  # creating the 3-dimensional array that is the jc model and init it with 0 as number of cars

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

    def update_snapshot(self):
        for i in CONF.ROADS:
            cars_in_dis = 0
            for j in self.roads[i].cars:
                if j.distance < CONF.CAMERA_DISTANCE:
                    cars_in_dis += 1

            enter = int(str(i).split(".")[0])
            exit_ = int(str(i).split(".")[1])
            self.snapshot[enter-1][exit_-1][0] = cars_in_dis
