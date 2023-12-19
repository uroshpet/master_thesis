import numpy as np
import cv2 as cv
import time
import random
import collections
from PIL import Image
from matplotlib import cm
import os
import urllib.request

class ObjectDetector_PP(object):

    def __init__(self, camera_dimentions, debug=True):
        
        #Load tiny yolo model
        with open('/home/pi/projects/donkeycar/donkeycar/parts/object_detector/classes.txt', 'r') as f:
            class_name = [cname.strip() for cname in f.readlines()]
        net = cv.dnn.readNet('/home/pi/projects/donkeycar/donkeycar/parts/object_detector/yolov4-tiny.weights', '/home/pi/projects/donkeycar/donkeycar/parts/object_detector/yolov4-tiny.cfg')
        #net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
        #net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)
        
        self.camera_dimentions = camera_dimentions
        self.detected_obj = None
        self.model = cv.dnn_DetectionModel(net)
        self.model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)
        self.img_arr = None
        self.debug = debug
        self.condition = 0

    def run_threaded(self,img_arr):
        self.img_arr = img_arr
        return self.detected_obj, self.img_arr

    def update(self): 
        while True:
            #start_recording = time.time()
            if self.img_arr is None:
                self.detected_obj = None
            else:
                classes, scores, boxes = self.model.detect(self.img_arr, 0.6, 0.4)
                for (classid, score, box) in zip(classes, scores, boxes):
                    if classid == 0:
                        self.condition = 0
                        self.detected_obj = (box[0] + int(box[2]/2), box[1]+box[3])
                        if(self.debug):
                            print("Found object!")
                        break
                    if self.debug:
                        print("Object not found!")
                #print(f"Object detector inference = {time.time() - start_recording}")
                self.condition += 1
                if(self.condition < 5):
                     cv.circle(self.img_arr, self.detected_obj ,5, color = (255,0,0), thickness= -1) #Draw circle on detected object for the next 5 frames regardless of detected status
