import pickle
import socket
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import sys
import time

global camera_dimentions, initial_pose, control_point, quality, server_socket
camera_dimentions = (416,416)
initial_pose = np.array([int(camera_dimentions[0]/2),camera_dimentions[1]])
control_point = np.array([int(camera_dimentions[0]/2), int(camera_dimentions[1]/2)])
quality = 10


def detect_object(model, img_arr):
    classes, scores, boxes = model.detect(img_arr, 0.2, 0.4)
    for (classid, score, box) in zip(classes, scores, boxes):
        if classid == 0:
            detected_obj = (box[0] + int(box[2]/2), box[1]+box[3])
            if (detected_obj[0] > camera_dimentions[0]* 0.45 and detected_obj[0] < camera_dimentions[0]*0.55) and (detected_obj[1] < camera_dimentions[1]* 0.50 and detected_obj[1] > camera_dimentions[1]*0.45):
                print("Reached object!")
                #self.detected_obj = None
                return detected_obj
            return detected_obj
        
def bezier_curve(x, start_point, control_point, end_point):
        return (1-x)**2 * start_point + 2 * (1-x) * x * control_point + x**2 * end_point

def generate_trajectory(detected_object):
    bezier_points = np.linspace(0, 1, quality)
    points = np.array([bezier_curve(bezier_point, initial_pose, control_point, np.array([detected_object[0],detected_object[1]])) for bezier_point in bezier_points])
    return points

def main():
    global server_socket

    # Set the host and port to listen on
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)

    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()


    #Load model for object detection

    with open('classes.txt', 'r') as f:
            class_name = [cname.strip() for cname in f.readlines()]    
    net = cv.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')
    #net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
    #net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)
    model = cv.dnn_DetectionModel(net)
    model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)
    print("Model loaded")
    buffer = b""
    
    #Set logic for drawing the trajectory
    fig, ax = plt.subplots()
    img_plot = ax.imshow(np.zeros((1, 1, 3)), cmap='gray')  # Initialize with an empty image
    curve_line, = ax.plot([], [], 'ro-', label='Bezier Curve Points')
    ax.set_xlim(0, 416)
    ax.set_ylim(416, 0)
    ax.set_aspect('equal', adjustable='box')

    plt.title('Received Image')
    plt.show(block=False)
    #start_timing_recieve = 0

    while True:
        # Calculate how fast the network recieved the data
        #if start_timing_recieve == 0:
        #    start_time = time.time()
        #    start_timing_recieve = 1
        
        #Logic to wait for data to be sent
        recieved_data = client_socket.recv(4096)
        
        if not recieved_data:
             continue
        
        buffer += recieved_data

        try:
            received_array = pickle.loads(buffer) #Attemt to recieve image, if not all image recieved repeat from the while llop on line 79
            #start_timing_recieve = 0
            #print(f"Recieved image in {time.time()-start_time} seconds")
            detected_object = detect_object(model,received_array)

            if(detected_object is None):
                ax.clear()
                ax.imshow(received_array, cmap='gray', extent=(0,416,416,0), origin='upper')
                plt.draw()
                plt.pause(0.01)
                response_to_client = pickle.dumps([1])
                client_socket.sendall(response_to_client) # Let the client know that no object is detected therfore no trajectory can be created
                buffer = b""
                continue

            trajectory = generate_trajectory(detected_object)
            ax.clear()
            ax.plot(trajectory[:, 0], trajectory[:, 1], color='green', marker='o')
            ax.imshow(received_array, cmap='gray', extent=(0,416,416,0), origin='upper') #Show the generated trajectory on the image recieved
            plt.draw()
            plt.pause(0.01)
            client_socket.sendall(pickle.dumps(trajectory)) # Send the client the generated trajectory

            buffer = b""  # Reset the buffer after successful deserialization

        except pickle.UnpicklingError as e:
            #print(f"Error during unpickling: {e}")
            # Data incomplete, keep sending untill it is
            continue

if __name__ == "__main__":
    try:
        while True:
            main()
    except KeyboardInterrupt:
        server_socket.close() # Close socket after the program is closed
        exit(0)
    
