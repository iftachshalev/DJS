from vehicle import *
from random import randint


class Road:

    SECONDS_BETWEEN_CARS_GREEN = 2

    def __init__(self, num_cars):
        self.cars = self.set_cars(num_cars)
        self.passed = []

    @staticmethod
    def set_cars(num_cars):  # returns a list of car objects
        return [Vehicle((randint(10, 1000)//10)*10) for i in range(num_cars)]

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
