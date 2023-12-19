import numpy as np
import cv2 as cv
import time
import random
import collections
from PIL import Image
from matplotlib import cm
import os
import urllib.request


class TrajectoryCreator(object):

    def __init__(self, camera_dimensions, quality, debug=False):

        self.control_point = (int(camera_dimensions[0]/2), int(camera_dimensions[1]/2))
        self.initial_pose = (int(camera_dimensions[0]/2), int(camera_dimensions[1]))
        self.detected_object = None
        self.trajectory = None
        self.quality = quality
        self.img_arr = None
    
    def bezier_curve(self, x, start_point, control_point, end_point):
        x = float(x)
        return (1-x)**2 * np.array(start_point,dtype = float) + 2 * (1-x) * x * np.array(control_point,dtype=float) + x**2 * np.array(end_point,dtype=float)

    def generate_trajectory(self):
        t_points = np.linspace(0, 1, self.quality)
        points = np.array([self.bezier_curve(t, self.initial_pose, self.control_point, self.detected_object) for t in t_points])
        return points
    
    def update(self):
        while True:
            if self.detected_object is None:
                self.trajectory = None
            else:
                start_time = time.time()
                self.trajectory = self.generate_trajectory()
                #cv.drawContours(self.img_arr, [self.trajectory], 0, (255,255,255),2)
                #print(f"Trajectory creator inference = {time.time() - start_time}")
    def run_threaded(self, detected_obj, img_arr):
        self.detected_object = detected_obj
        self.img_arr = img_arr
        return self.trajectory, self.img_arr
