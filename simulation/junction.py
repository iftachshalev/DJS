from road import *


class Junction:

    def __init__(self):
        self.combinations = [[6.3, 6.1, 4.5], [2.3, 2.5, 4.5], [2.3, 4.1, 4.5]]
        self.roads = [Road(i) for i in [2.3, 2.5, 4.1, 4.5, 6.1, 6.3]]

    def advance_junction(self, sec):
        pass
