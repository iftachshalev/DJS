from junction import *


def check_road(red_time, green_time, n):
    road = Road(2.3)
    print("starting position for road 23:")
    print(road)
    for k in range(n):
        print(f"advancing red cars for {red_time} sec:")
        road.advance_red_road(red_time)
        print(road)
        print(f"advancing green cars for {green_time} sec:")
        road.advance_green_road(green_time)
        print(road)


def check_junction():
    jc = Junction(True)
    print(jc)
    for i in range(100):
        jc.advance_junction(2)
        print(jc)


# check_road(5, 2, 50)
check_junction()
