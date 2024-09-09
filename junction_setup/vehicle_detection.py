import cv2
import random


class VehicleDetection:
    
    def __init__(self):
        """
        init the traned module
        """

        self.cars_cascade = cv2.CascadeClassifier('haarcascade_car.xml')

    def detect_cars(self, frame):

        """
        needs to be implemented with a trained module
        """
        cars = self.cars_cascade.detectMultiScale(frame, 1.15, 4)
        car_count = len(cars)
        for (x, y, w, h) in cars:
            cv2.rectangle(frame, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)
        return frame, car_count

    def count_vehicles(self, img):
        """
        returns the number of cars in a pic
        """
        frame, cars = self.detect_cars(img)
        useless, cars = 0, random.randint(0, 12)  # for we overwrite this until a model will be created

        # cv2.imshow('image', frame)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return cars
