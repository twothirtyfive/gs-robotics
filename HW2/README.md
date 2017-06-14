This is the lab 2 submission for Robotics Dream Team of General Studies.
Members: Julian Kocher (jk3813), Najlaa Bouras (nb2749), Michael Falkenstein (maf2233)

Code requires the included control.py, as it has been modified from the original.
Code also requires the most up-to-date version of gopigo.py, found on the GoPiGo github.

Link to Bug2 video: https://youtu.be/QovwDTMC1RU

Our robot is programmed to record its starting position, then moves forward until it reaches an obstacle. It then turns left, and then position and orientation are recorded.
It then travels along the obstacle until it reaches a corner. It moves forward the length of itself, rotates, and stores this location and orientation.
It continues to do this until it is oriented towards the m-line. If it is oriented towards the m-line, the robot will move either until it reaches the end of the obstacle or the m-line is reached.
Once the robot reaches the m-line, it finds the goal and orients itself towards it. It then repeats the process of navigating the next obstacle, or it reaches the goal.
