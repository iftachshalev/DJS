

class ActionDecider:

    def __init__(self, combs):
        self.combinations = combs

    def sum_of_cars_in_combs(self, road_cars_dict):
        arr = []
        for i in self.combinations:
            sum_ = 0
            for j in i:
                sum_ += road_cars_dict[j]
            arr.append(sum_)
        return arr

    def most_cars(self, road_cars_dict, green_comb, green_time):
        sum_comb = self.sum_of_cars_in_combs(road_cars_dict)

        hpc_car_num = max(sum_comb)
        hpc_idx = sum_comb.index(hpc_car_num)

        if len(set(sum_comb)) == 1 or green_time < 10:
            return green_comb

        return self.combinations[hpc_idx]
