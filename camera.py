import cv2


class Camera:
    
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
    
    def read_img(self):  # will take a pic on the rpi cam
        # img = cv2.imread('data/for_now.jpg')
        ret, img = self.cam.read()
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return img

