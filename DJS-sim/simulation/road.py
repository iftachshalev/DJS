from vehicle import *
from random import randint


class Road:

    CARS_LIVING_PER_SEC = 3  # [s] cant be 0. 1 over this value is how many cars get out every sec

    def __init__(self, num_cars, max_dis):
        self.cars = self.set_cars(num_cars, max_dis)
        self.passed = []
        self.green_time = 0

    @staticmethod
    def set_cars(num_cars, max_dis):  # returns a list of car objects
        return [Vehicle(randint(0, max_dis-1)) for i in range(num_cars)]

    def advance_red_road(self, sec):
        for i in self.cars:
            i.advance(sec)

    def advance_green_road(self, tick):  # GT is given before += tick
        # 1. advance red for sec long.
        self.advance_red_road(tick)

        # 2. remove cars according to sec.
        passed_before = int(self.green_time*self.CARS_LIVING_PER_SEC)
        should_pass = int((self.green_time + tick)*self.CARS_LIVING_PER_SEC) - passed_before
        self.remove_n_car(should_pass)

    def remove_n_car(self, n):

        for i in range(n):
            if len(self.cars) == 0:
                break

            time_to_remove = max([i.time_since_arrival for i in self.cars])

            if time_to_remove != -1:
                for car in self.cars:
                    if car.time_since_arrival == time_to_remove:
                        self.passed.append(car)
                        self.cars.remove(car)
                        break

    def __repr__(self):
        s = ""
        for i, car in enumerate(self.cars):

            s += f"\tcar id {car.vehicle_id} ==> " + car.__repr__() + "\n"
        return s
