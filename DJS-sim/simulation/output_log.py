from config_handler import *


class Output:
    def __init__(self):
        pass
    def start_of_simulation(self, jc):
        print(f"starting point:\n")
        self.print_state(jc)

    def end_of_simulation(self, jc):
        print(f"***ENDED ON TIME: {jc.sim_time}***\n"
              f"\t>>>total cars that passed:        |  {sum([len(j.passed) for j in jc.roads.values()])}\n"
              f"\t>>>total cars that didn't pass:   |  {sum([len(j.cars) for j in jc.roads.values()])}\n"
              f"\t>>>total switches:                |  {jc.switched}\n")

    def print_state(self, jc):

        meter_char_sign = 10  # cannot be 0

        print(f"after {jc.sim_time} seconds, this is the state:")
        print(f"green combination: {CONF.COMBINATIONS[jc.green_comb]} for {jc.jc_green_time} seconds")

        for i in CONF.ROADS:

            if i in CONF.COMBINATIONS[jc.green_comb]:
                print(f"{bcolors.OKGREEN}ROAD {i}: {bcolors.ENDC}", end="")
            else:
                print(f"{bcolors.FAIL}ROAD {i}: {bcolors.ENDC}", end="")

            road_str = "-"*(int(CONF.MAX_VEHICLE_DISTANCE/meter_char_sign) + 1)  # +1 for no index out of range

            for j in jc.roads[i].cars:
                place_idx = int(j.distance/meter_char_sign)

                if road_str[place_idx] == "-":
                    road_str = road_str[:place_idx] + "1" + road_str[place_idx+1:]
                elif road_str[place_idx] == "@":
                    pass
                else:
                    if int(road_str[place_idx]) < 9:
                        road_str = road_str[:place_idx] + str(int(road_str[place_idx]) + 1) + road_str[place_idx + 1:]
                    else:
                        road_str = road_str[:place_idx] + "@" + road_str[place_idx + 1:]

            if CONF.CAMERA_DISTANCE >= CONF.MAX_VEHICLE_DISTANCE:
                pass
            else:
                camera_idx = int(CONF.CAMERA_DISTANCE/meter_char_sign)  # accurate print - it should be divisible
                road_str = road_str[:camera_idx] + f"{bcolors.ENDC}" + road_str[camera_idx:]

            road_str = f"{bcolors.OKBLUE}{road_str}|==> {len(jc.roads[i].cars)} cars; GT - {jc.roads[i].green_time} [s]"

            print(road_str)
        jc.update_snapshot()
        print(nice_mat(jc.snapshot))

        print("\n\n\n")

    def print_str(self, str_):
        print(str_)


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


# def __repr__(self):
#
#     s = ""
#     for i in self.roads.values():
#         if self.detailed_print:
#             s += (f"ROAD {list(self.roads.keys())[list(self.roads.values()).index(i)]}: there are {len(i.cars)} "
#                   f"cars and {len(i.passed)} passed\n")
#             s += i.__repr__()
#         else:
#             s += (f"ROAD {list(self.roads.keys())[list(self.roads.values()).index(i)]}: there are {len(i.cars)} "
#                   f"cars and {len(i.passed)} passed\n")
#     s += f"time since init: {self.sim_time}\ngreen comb {CONF.COMBINATIONS[self.green_comb]}\n\n"
#     s += f"the junction snapshot: \n{nice_mat(self.snapshot)}\n\n\n"
#     return s