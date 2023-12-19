import numpy as np
import cv2 as cv
import time
import random
import collections
from PIL import Image
from matplotlib import cm
import os
import urllib.request


class ObjectDetectorMobileSSD(object):

    def download_file(self, url, filename):
        if not os.path.isfile(filename):
            urllib.request.urlretrieve(url, filename)

    def __init__(self, debug=False):
        
        #Load model NB! Change path to match the models
        with open('/home/pi/projects/donkeycar/donkeycar/parts/object_detector/classes_mobilenet_ssd.txt', 'r') as f:
            class_name = [cname.strip() for cname in f.readlines()]
        
        self.model = cv.dnn.readNetFromCaffe('/home/pi/projects/donkeycar/donkeycar/parts/object_detector/MobileNetSSD_deploy.prototxt', '/home/pi/projects/donkeycar/donkeycar/parts/object_detector/MobileNetSSD_deploy.caffemodel')
        
        self.current_frame = 0
        self.total_fps = 0
        self.img_arr = None
        self.detected_objects = None

    def run_threaded(self, img_arr):
        self.img_arr = img_arr
        return self.detected_objects

    def update(self):
        while True:
            if self.img_arr is None:
                continue
            else:
                blob = cv.dnn.blobFromImage(cv.resize(self.img_arr,(300,300)), 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
                self.model.setInput(blob)
                self.current_frame += 1
                start_time = time.time()
                self.detected_objects = self.model.forward()
                self.total_fps += 1/(time.time()-start_time)
                print(f"MobileNetSSD avg fps = {self.total_fps/self.current_frame}")
