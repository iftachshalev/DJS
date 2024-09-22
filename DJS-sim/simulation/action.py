

class ActionDecider:

    def __init__(self, combs):
        self.combinations = combs

    def most_cars(self, cars_in_combs, green_comb, green_time):

        hpc_car_num = max(cars_in_combs)
        hpc_idx = cars_in_combs.index(hpc_car_num)

        if len(set(cars_in_combs)) == 1:
            return green_comb

        return hpc_idx
