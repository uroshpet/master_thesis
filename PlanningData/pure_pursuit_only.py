import numpy as np
import cv2 as cv
import time
import random
import collections
from PIL import Image
from matplotlib import cm
import os
import urllib.request
import socket
import pickle
import math
import sys
import select

class PurePursuitOnly(object):

    def __init__(self, lookahead_distance, camera_dimentions, host, debug=False):
        self.lookahead_distance = 9 # Set lookahead distance of the pure pursiuit controller NB! Must be less than the quality set in the server!!!
        self.initial_pose = (camera_dimentions[0] / 2, camera_dimentions[1])
        self.steering = 0.0
        self.host = host
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.client_socket.connect((host, 8080))
        self.image_arr = None

    def update(self):
        while True:

            if self.image_arr is None:
                continue
            
            # Send image to server
            data_to_send = pickle.dumps(self.image_arr)
            self.client_socket.sendall(data_to_send)
            start_timing_recieve = 0
            buffer = b""
            
            while True:
                if start_timing_recieve == 0:
                   start_time = time.time()
                   start_timing_recieve = 1
                # Wait for response from server

                trajectory_data = self.client_socket.recv(2048)
                if not trajectory_data:
                    continue
                buffer += trajectory_data
                try:
                    trajectory = pickle.loads(buffer)
                    buffer = b"" 
                    break

                except pickle.UnpicklingError as e:
                    # Data incomplete, keep recieving
                    continue
            #print(f"total recieve time = {time.time() - start_time}s")
            if np.size(trajectory) == 1:
                continue # No object found to follow, send image again
            else:
                    lookahead_point = trajectory[self.lookahead_distance]
                    angle_to_take = np.arctan2(lookahead_point[0] - self.initial_pose[0], self.initial_pose[1] - lookahead_point[1])
                    self.steering = math.degrees(angle_to_take)/90
                    #total_time = time.time() - start_time
                    #print(f"Total inference time = {total_time}s")
                    start_timing_recieve = 0
                    #print(f"Fps = {1/(time.time()-start_time)}")
                    #print(f"Set steering value to {self.steering}")
                    if(self.steering > 1): # Edge cases, might not happen
                        self.steering = 1.0
                    elif(self.steering <-1):
                        self.steering = -1.0
    
    def run_threaded(self, image_arr):
        self.image_arr = image_arr
        return self.steering
    
