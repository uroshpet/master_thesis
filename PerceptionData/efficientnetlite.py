import numpy as np
import cv2 as cv
import time
import random
import collections
from PIL import Image
from matplotlib import cm
import os
import urllib.request
import tensorflow as tf


class ObjectDetectorEfficientNetLite(object):

    def __init__(self, debug=False):
        
        # Load model NB! Change path to match the .tflite model loaded
        self.model = tf.lite.Interpreter(model_path='/home/pi/projects/donkeycar/donkeycar/parts/object_detector/efficientnet_lite.tflite')
        self.model.allocate_tensors()
        self.input_tensor_index = self.model.get_input_details()[0]['index']
        self.output = self.model.tensor(self.model.get_output_details()[0]['index'])
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
                input_data = cv.resize(self.img_arr, (self.model.get_input_details()[0]['shape'][2], self.model.get_input_details()[0]['shape'][1]))
                input_data = np.expand_dims(input_data, axis=0)
                input_data = (input_data / 255.0).astype(np.uint8)
                self.model.set_tensor(self.input_tensor_index, input_data)
                self.model.invoke()
                self.total_fps += 1/(time.time()-start_time)
                print(f"EfficientNet avg fps = {self.total_fps/self.current_frame}")
