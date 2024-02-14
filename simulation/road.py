from vehicle import *


class Road:

    SECONDS_BETWEEN_CARS_GREEN = 2

    def __init__(self, road_name):
        self.road_name = road_name  # enter.exit
        self.cars = [Vehicle(121), Vehicle(900), Vehicle(600), Vehicle(200), Vehicle(500), Vehicle(1200), Vehicle(700)]
        self.passed = []

    def advance_red_road(self, sec):
        for i in self.cars:
            i.advance(sec)

    def advance_green_road(self, sec):
        # 1. advance red for sec long.
        self.advance_red_road(sec)

        # 2. remove cars according to sec.
        car_pass = int(sec)//self.SECONDS_BETWEEN_CARS_GREEN + 1
        self.remove_n_car(car_pass)

    def remove_n_car(self, n):

        for i in range(n):
            if len(self.cars) == 0:
                break

            time_to_remove = max([i.time_since_arrival for i in self.cars])

            if time_to_remove != -1:
                for j in self.cars:
                    if j.time_since_arrival == time_to_remove:
                        self.passed.append(j)
                        self.cars.remove(j)
                        break

    def __repr__(self):
        s = ""
        for i, car in enumerate(self.passed):

            s += f"for car number id {car.vehicle_id} ==> " + car.__repr__() + "\n"
        return f"for road {self.road_name}:\n"+s
