import random


class Vehicle:

    def __init__(self, distance=100, speed=36, vehicle_id=None):  # distance[M] speed[kph]
        self.distance = distance
        self.v = int(speed/3.6)  # convertion to [M/S] and rounding
        self.time_since_arrival = -1  # -1 until the car reaches the junction
        if not vehicle_id:
            self.vehicle_id = random.randint(1000, 9999)
        else:
            self.vehicle_id = vehicle_id

    def advance(self, sec):

        if self.distance - sec * self.v > 0:
            self.distance -= sec * self.v

        else:
            if self.time_since_arrival == -1:
                sec_till_arrival = self.distance/self.v
                self.time_since_arrival = sec - sec_till_arrival
                self.distance = 0
            else:
                self.time_since_arrival += sec

    def __repr__(self):
        return f"speed: {self.v}[mps], distance: {self.distance:.2f}[m] time since arrival {self.time_since_arrival}[s]"
