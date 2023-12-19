import numpy as np
import cv2 as cv
import time
import random
import collections
from PIL import Image
from matplotlib import cm
import os
import urllib.request
import math


class PurePursuit(object):

    def __init__(self, lookahead_distance, camera_dimentions, debug=False):
        self.lookahead_distance = lookahead_distance
        self.trajectory = None
        self.initial_pose = (int(camera_dimentions[0] / 2), camera_dimentions[1])
        self.steering = 0.0
    
    def update(self):
        while True:
            if self.trajectory is None or np.size(self.trajectory) < self.lookahead_distance:
                self.steering = 0.0
            else:
                lookahead_point = self.trajectory[self.lookahead_distance]
                # Calulate the angle needed to steer the car in the direction of the detected object
                angle_to_take = math.atan2(self.initial_pose[1] - lookahead_point[1], lookahead_point[0] - self.initial_pose[0])
                self.steering = angle_to_take/90
                if(self.steering > 1):
                   self.steering = 1.0
                elif(self.steering <-1):
                   self.steering = -1.0
    
    def run_threaded(self, trajectory):
        self.trajectory = trajectory
        return self.steering
