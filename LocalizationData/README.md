1. install cartographer and hector slam on the host machine following the instructions on the developer websites
2. copy Cartographer/my_robot.lua to /home/uroshpet/Master_thesis_ROS_workspaces/cartographer_ws/install_isolated/share/cartographer_ros/configuration_files
3. copy Cartographer/my_robot.launch to /home/uroshpet/Master_thesis_ROS_workspaces/cartographer_ws/install_isolated/share/cartographer_ros/lauch
4. copy Cartographer/donkey_2d.urdf to /home/uroshpet/Master_thesis_ROS_workspaces/cartographer_ws/install_isolated/share/cartographer_ros/urdf
5. Copy Hector_Slam/mapping_default.launch to hector_slam/hector_mapping/launch

# Both SLAM algorithms

1. Connect donkeycar and server to same network
2. Run commangd export ROS_MASTER_URI=http://ip_of_host_machine:11311/ on all machines
3. Run command export ROS_IP=ip_of_donkey_car on donkeycar
4. Run command sudo ntpd ip_of_host_machine on donkeycar
5. Run command roscore on host machine



# Cartographer
6. launch in 2 windows commands roslaunch rplidar_ros rplidar.launch and roslaunch mpu9250-driver mpu9250.launch on donkey car

7. roslaunch cartographer_ros my_robot.launch  on host machine, open rviz and add map and tf.
8. Drive the car around

# Hector SLAM
6. Run command roslaunch rplidar_ros rplidar.launch on donkeycar
7. Run command roslaunch hector_slam_launch tutorial.launch on host machine, open rviz and add map and tf.
8. Drive the car around


NB! The IMU needs to possibly be calibrated, run the calibrate.py script in the imusensor package in the ros-mpu9250-ahrs package to calibrate.
