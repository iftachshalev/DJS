import yaml

# make sure:


class Config:
    
    def __init__(self):
        with open("config.yaml") as stream:
            try:
                data = yaml.safe_load(stream)
                self.pic_per_sec = data["pic_per_sec"]
                self.roads = data["roads"]
                self.combs = data["combs"]
                # print(data)
            except yaml.YAMLError as exc:
                print(exc)
