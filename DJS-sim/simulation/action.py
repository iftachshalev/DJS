

class ActionDecider:

    def __init__(self, combs):
        self.combinations = combs

    def most_cars(self, road_cars_dict, green_comb, green_time):

        hpc_car_num = max(road_cars_dict)
        hpc_idx = road_cars_dict.index(hpc_car_num)

        if len(set(road_cars_dict)) == 1:
            return green_comb

        return self.combinations[hpc_idx]
