from config_handler import *
import logging as log
from math import ceil


class Output:

    METERS_PER_SIGN = 10  # cannot be 0

    def __init__(self, screen=True, log_file=False):
        self.screen = screen
        self.log_file = log_file

    def start_of_simulation(self, jc):
        self.print_str(f"starting point:\n")
        self.print_state(jc)

    def end_of_simulation(self, jc):
        self.print_str(f"***ENDED ON TIME: {jc.sim_time}***\n"
                       f"\t>>>total cars that passed:        |  {sum([len(j.passed) for j in jc.roads.values()])}\n"
                       f"\t>>>total cars that didn't pass:   |  {sum([len(j.cars) for j in jc.roads.values()])}\n"
                       f"\t>>>total switches:                |  {jc.switched}\n")

    def print_state(self, jc):
        state = (f"after {jc.sim_time} seconds, this is the state:\n"
                 f"green combination: {CONF.COMBINATIONS[jc.green_comb]} for {jc.jc_green_time} seconds\n")

        for i in CONF.ROADS:

            if i in CONF.COMBINATIONS[jc.green_comb]:
                state += f"{bcolors.OKGREEN}ROAD {i}: {bcolors.ENDC}"
            else:
                state += f"{bcolors.FAIL}ROAD {i}: {bcolors.ENDC}"

            road_str = "-" * ceil(CONF.MAX_VEHICLE_DISTANCE / self.METERS_PER_SIGN)
            road_str = self.add_cars(road_str, jc, i)
            road_str = self.add_cam_dis(road_str)
            road_str = f"{road_str}|==> {len(jc.roads[i].cars)} cars; GT - {jc.roads[i].green_time} [s]\n"

            state += road_str

        self.print_str(state[:-1])
        jc.update_snapshot()
        self.print_str(f"{nice_mat(jc.snapshot)}\n\n")

    def add_cars(self, road_str, jc, road):
        for j in jc.roads[road].cars:
            place_idx = int(j.distance / self.METERS_PER_SIGN)

            if road_str[place_idx] == "-":
                road_str = road_str[:place_idx] + "1" + road_str[place_idx + 1:]
            elif road_str[place_idx] == "@":
                pass
            else:
                if int(road_str[place_idx]) < 9:
                    road_str = road_str[:place_idx] + str(int(road_str[place_idx]) + 1) + road_str[place_idx + 1:]
                else:
                    road_str = road_str[:place_idx] + "@" + road_str[place_idx + 1:]
        return road_str

    def add_cam_dis(self, road_str):
        if CONF.CAMERA_DISTANCE > CONF.MAX_VEHICLE_DISTANCE or CONF.CAMERA_DISTANCE < 0:
            camera_idx = len(road_str)
        else:
            camera_idx = int(CONF.CAMERA_DISTANCE / self.METERS_PER_SIGN)  # accurate print - it should be divisible
        road_str = road_str[:camera_idx] + f"{bcolors.ENDC}" + road_str[camera_idx:]
        road_str = str(bcolors.OKBLUE) + road_str
        return road_str

    def print_str(self, str_):
        if self.screen:
            print(str_)
        if self.log_file:
            log.info(str_.replace(bcolors.OKGREEN, "")
                     .replace(bcolors.OKBLUE, "")
                     .replace(bcolors.ENDC, "")
                     .replace(bcolors.FAIL, ""))


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


log.basicConfig(level=log.DEBUG,
                format='%(levelname)s - %(message)s',
                filename='app.log',
                filemode='w')
