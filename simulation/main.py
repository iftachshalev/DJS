from junction import *


road = Road("23")
print(road)
for k in range(60):
    road.advance_green_road(1)
    print("advancing cars....")
    print(road)
