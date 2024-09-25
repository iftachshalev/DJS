

class ActionDecider:

    def __init__(self, combs):
        self.combinations = combs  # to remove

    def most_cars(self, snap, GC, GT):

        max_comb = num_of_combs(snap)
        cars_in_comb = get_num_cars(snap, max_comb)
        return cars_in_comb.index(max(cars_in_comb))


def num_of_combs(mat):
    combs = set()
    for i in mat:
        for j in i:
            if j:
                combs.update(set(j[1:]))
    return max(combs)


def get_num_cars(mat, max_comb):
    cars = [0 for i in range(max_comb+1)]
    for i in mat:
        for road_arr in i:
            if road_arr:
                for comb in road_arr[1:]:
                    cars[comb] += road_arr[0]
    return cars
