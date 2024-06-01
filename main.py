import time
from config_handler import Config
from camera import Camera
from utils import Utils
from vehicle_detection import VehicleDetection
from RL_model import RL


config = Config()
cam = Camera()
utils = Utils()
v_detector = VehicleDetection()
model = RL()


junction_state = {
    "vehicle_in_combs": [0 for i in config.combs],
    "active_comb": 0,
    "green_time": 0
}
round_ = 1

print(f"roads: {config.roads}, combs: {config.combs}")
print(f"start: junction state: {junction_state}\n\n")

while True:

    print(f"round: {round_}")

    # 1. read img from cam
    pic = cam.read_img()

    # 2. from that img get image for each road
    j_pics = utils.parse_img(pic, len(config.roads))

    # 3. get the number of cars in each road. array set the same way as config.roads
    vehicle_count = [v_detector.count_vehicles(i) for i in j_pics]
    print(f"vehicle_count: {vehicle_count}")
    junction_state["vehicle_in_combs"] = utils.calc_vehicle_in_comb(config.roads, vehicle_count, config.combs)

    # at this point we have an updated state of the junction, and we are ready to feed it to the model
    print(f"junction state: {junction_state}")

    # getting an action from the model
    next_comb = model.action(junction_state)
    print(f"next comb: {next_comb}\n\n")

    # implement the action
    if junction_state["active_comb"] != next_comb:
        junction_state["active_comb"] = next_comb
        junction_state["green_time"] = 0
        utils.physical_implementation(next_comb)  # needed to be done on a different thread

    time.sleep(1/config.pic_per_sec)
    junction_state["green_time"] += 1/config.pic_per_sec
    round_ += 1



