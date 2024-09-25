import yaml


class Config:
    
    def __init__(self):
        with open("config.yaml") as stream:
            try:
                data = yaml.safe_load(stream)
                self.ROADS = data["ROADS"]
                self.COMBINATIONS = data["COMBINATIONS"]
                self.SWITCH_PENALTY = data["SWITCH_PENALTY"]
                self.CAMERA_DISTANCE = data["CAMERA_DISTANCE"]
                self.NUM_CARS = data["NUM_CARS"]
                self.MAX_VEHICLE_DISTANCE = data["MAX_VEHICLE_DISTANCE"]

            except yaml.YAMLError as exc:
                print(exc)


CONF = Config()
