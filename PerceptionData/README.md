Copy all files to projects/donkeycar/donkeycar/object_detector
Changee all paths in the .py scripts to match the paths of the donkeycar
Copy manage_steering.py to mycar directory

1. Set STOP_SIGN_DETECTOR parameter to true to load models
2. In manage_steering.py navigate to cfg.STOP_SIGN detector and uncomment(comment) the model you wish to load (that will be the from line and the V.add line)
3. Change the image resolution in the mycar/myconfig to match the models (416x416 for tinyyolo, 300x300 for efficientnet and mobilenetssd
3. run command python manage_steering.py drive to start the experiment
