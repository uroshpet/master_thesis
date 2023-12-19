import numpy as np
import cv2 as cv
import time
import random
import collections
from PIL import Image
from matplotlib import cm
import os
import urllib.request


class ObjectDetectorTinyYolo(object):

    def __init__(self, debug=False):
        with open('/home/pi/projects/donkeycar/donkeycar/parts/object_detector/classes_yolov4-tiny.txt', 'r') as f:
            class_name = [cname.strip() for cname in f.readlines()]
        net = cv.dnn.readNet('/home/pi/projects/donkeycar/donkeycar/parts/object_detector/yolov4-tiny.weights', '/home/pi/projects/donkeycar/donkeycar/parts/object_detector/yolov4-tiny.cfg')
        self.model = cv.dnn_DetectionModel(net)
        self.model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)
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
                self.current_frame += 1
                start_time = time.time()
                detected_objects = self.model.detect(self.img_arr, 0.4, 0.4)
                self.total_fps += 1/(time.time()-start_time)
                print(f"TinyYolo avg fps = {self.total_fps/self.current_frame}")
