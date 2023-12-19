Instructions to start pure pursuit experiment:

Connect the server and client to the same network
Copy classes.txt, object_detector_pp.py, pure_pursuit.py, pure_pursuit_only.py, trajectory_creator.py, yolov4-tiny.cfg, yolov4-tiny.weights to projects/donkeycar/donkeycar/parts/pure_pursuit folder
Copy manage_pure_pursuit.py and manage_pure_pursuit_only.py to mycar folder

In the mycar/myconfig.py file change the variables of the pure pursuit controller to match the desired quality (only for full pure pursuit)

Change the paths in the object_detector_pp.py to match the model path,the lookahead distance in pure_pursuit_only.py to match the server quality and the quality in trajectory_creator_newer.py to set the quality of the trajectory

# Pure pursuit fully on donkeycar

1. Run the command python manage_pure_pursuit.py drive on the donkey car to start the pure pursuit purely on the donkey car

# Pure pursuit partially on donkeycar

1. Run the command python trajectory_creator_newer.py to start the server
2. Run the command python manage_pure_pursuit_only.py drive --js to start the client
3. Set the drive to local_pilot or local_angle to visualize the steering
