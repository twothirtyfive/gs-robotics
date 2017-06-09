# Implement a BUG2 algorithm to move the GoPiGo from a designated starting point to a goal point in an environment. 
# Your robot should start out along the straight line path from start to goal (the M Line). Using the ultrasound sensor, 
# if it sees any obstacles along the way, it will invoke a perimeter following behavior until the M Line is reacquired 
# and the robot again starts out for the goal point along the M Line. When the goal point is reached, the robot will stop.

# Assume a trajectory from a start point to a goal point about 3 meters in front of the robot. Add 2-3 test obstacles 
# (garbage cans and cardboard boxes work well here!) that impede the path, requiring the GoPiGo to invoke BUG2 behavior.

# Your program should also map out your robot’s progress graphically, showing robot position and robot orientation 
# (robot pose) as it moves along (odometry). You should also display on the map locations where the ultrasound 
# sensor has seen an obstacle. A quick tutorial on python plotting using matplotlib (installed on your RaspberryPi) 
# is here: http://matplotlib.org/users/pyplot_tutorial.htm (Links to an external site.)Links to an external site.l 
# (Links to an external site.)Links to an external site.

# Note: this mapping may slow down your communication and affect performance of your robot. If you are experiencing this, 
# then cache the pose and obstacle information and map it out after the robot stops.

# Video your robot as it does its movement from start to finish, avoiding obstacles. Post the video to youtube and 
# include the link in your handed in README file. Note: Your BUG2 algorithm should also be aware when it is trapped 
# inside of an obstacle and report this. Make sure you test this part of your algorithm as well (no video required of 
# this). Hand in the usual code and README files, along with the link to the robot video on youtube.