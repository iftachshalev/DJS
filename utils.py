

class Utils:
    
    def __init__(self):
        pass
    
    def parse_img(self, img, num_roads):
        """
        dummy pursing - figure it out using vectors
        """
        imgs = []
        for i in range(0, num_roads):
            inner_img = img[len(img) // num_roads * i: len(img) // num_roads * (i + 1)]
            imgs.append(inner_img)
        return imgs

    def format_img(self, img):
        """
        returns formated image ready for the next stages
        """
        pass

    def calc_vehicle_in_comb(self, roads, vehicle_count, combs):
        combs_vehicles = []

        for i in combs:
            vehicles = 0
            for j in i:
                vehicles += vehicle_count[roads.index(j)]

            combs_vehicles.append(vehicles)

        return combs_vehicles

    def physical_implementation(self, action):
        pass

