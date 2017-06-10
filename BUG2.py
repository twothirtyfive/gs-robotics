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

#!/usr/bin/python
'''
This is inspired by both the Ultrasonic Basic Obstacle Avoider 
and Ultrasonic_Servo examples. 

Essentially, the gopigo should: 
  - Move fwd until it is within 20cm of an obstacle
  - Stop
  - Scan the room
  - Find a space between obstacles big enough to fit
  - Turn in that direction
  - Move fwd until it is within 20cm of an obstacle
  - Etc.
'''

from gopigo import *
from control import *
import math
import time

STOP_DIST=20 # Dist, in cm, before an obstacle to stop.
SAMPLES=4 # Number of sample readings to take for each reading.
INF=200 # Distance, in cm, to be considered infinity.
REPEAT=2
DELAY=.02

inline = False
abreast = False

def main():
    print "*** Starting BUG2 Example ***"
    start_left = enc_read(0)
    start_right = enc_read(1)
    move_until(5)

    delta_left_enc = enc_read(0) - start_left
    delta_right_enc = enc_read(1) - start_right
    print delta_left_enc
    print delta_right_enc
    my_turn()


    # for x in range(REPEAT):
    #     move(STOP_DIST)
    #     readings = scan_room()
    #     holes = findholes(readings)
    #     gaps = verify_holes(holes)
    #     if len(gaps) == 0:
    #         print "Nowhere to go!!"
    #         stop()
    #         exit()
    #     ## Choose the first gap found
    #     turn_to(gaps[0][0])
    # servo(90)
    stop()

def my_turn():
    servo(80)
    rdist = avg_us_dist()
    servo(90)
    mdist = avg_us_dist()
    servo(100)
    ldist = avg_us_dist()
    if ldist > mdist and rdist > mdist:
        deg = 90
    else:
        a = math.sqrt(ldist^2 + rdist^2 - 2*ldist*rdist*math.cos(20))
        beta = math.degrees(math.asin(ldist*math.sin(20)/a))
        deg = 180-beta

    turn('left',deg)

def move(min_dist):
    ## Set servo to point straight ahead
    servo(90)
    print "Moving Forward"
    while us_dist(15) > min_dist:
        fwd()
        time.sleep(.02)
    stop()
    print "Found obstacle"
    return

def turn_to(angle):
    '''
    Turn the GoPiGo to a specified angle where angle=0 is 90deg 
    the way to the right and angle=180 is 90deg to the left.
    The GoPiGo is currently pointing forward at angle==90.
    '''
    ## <0 is turn left, >0 is turn right.
    degs = angle-90
    print "Turning craft {} degrees".format(degs),
    if degs > 0:
        print "to the left"
        left_deg(degs)
    else:
        print "to the right"
        right_deg(degs)
    ## This sleep is really just for debugging so I can verify that it turned properly
    time.sleep(1)

def verify_holes(holes):
    '''
    A hole is a list of (angle,distance) tuples.
    To verify that a hole can fit the chassis,
    we need to calculate the distance between the 
    first and last tuple.
    Returns a list of (angle,gap distance) tuples.
    '''
    print "Verifying holes ... "
    gaps = []
    for hole in holes:
        print "  Hole:{}".format(hole),
        xy1 = calc_xy(hole[0])
        xy2 = calc_xy(hole[-1])
        gap = calc_gap(xy1,xy2)
        ang1 = hole[0][0]
        ang2 = hole[-1][0]
        middle_ang = (ang2 + ang1)/2
        print "ang:{},gap:{}".format(middle_ang,gap)   
        if gap >= CHASS_WID:
            print "    It's wide enough!"
            gaps.append((middle_ang,gap))
    return gaps

def findholes(readings):
    '''
    Each reading will be a (angle,dist) tuple giving
    the distance to an obstacle at the given angle.
    To find a hole, we want 3 consecutive INF readings.
    '''
    print "Processing readings to find holes...."
    print readings
    holes = []
    buf = []
    ## Previous non-INF reading
    prev = ()
    for (a,d) in readings:
        print "  {}:{}".format(a,d)
        if d < INF:
            ## If dist is not INF, then we've hit another
            ## obstacle, so reset the buffer.
            if len(buf) > 2:
                ## If the buffer has at least 3 INF readings,
                ## then record the hole.
                holes.append(buf)
                print "    Found a hole: {}:{}".format(a,d)
            buf = []
            continue
        ## Add reading to buffer
        buf.append((a,d))
    ## In case the last reading was INF
    if len(buf) > 2:
        holes.append(buf)
        print "    Found a hole: {}:{}".format(a,d)
    return holes

def scan_room():
    '''
    Start at 0 and move to 180 in increments.
    Angle required to fit chass @20cm away is:
        degrees(atan(CHASS_WID/20))
    Increments angles should be 1/2 of that.
    Looking for 3 consecutive readings of inf.
    3 misses won't guarantee a big enough hole
     because not every obstacle will be 20cm away,
     but it is a good place to start, and more
     importantly, gives us edges to use to 
     measure.
    
    Return list of (angle,dist).
    '''
    ret = []
    inc = int(math.degrees(math.atan(CHASS_WID/20)))
    print "Scanning room in {} degree increments".format(inc)
    for ang in range(0,180,inc):
        print "  Setting angle to {} ... ".format(ang),
        ## resetting ang because I've seen issues with 0 and 180
        if ang == 0: ang = 1
        if ang == 180: ang = 179
        servo(ang)
        buf=[]
        for i in range(SAMPLES):
            dist=us_dist(15)
            print dist,
            if dist<INF and dist>=0:
                buf.append(dist)
            else:
                buf.append(INF)
        print
        ave = math.fsum(buf)/len(buf)
        print "  dist={}".format(ave)
        ret.append((ang,ave))
        ## Still having issues with inconsistent readings.
        ## e.g. 
        ##  Setting angle to   0 ...    18   19 218 49
        ##  Setting angle to 170 ...  1000 1000  45 46
        time.sleep(DELAY)
    ## Reset servo to face front
    servo(90)
    return ret

def calc_xy(meas):
    '''
    Given an angle and distance, return (x,y) tuple.
    x = dist*cos(radians(angle))
    y = dist*sin(radians(angle))
    '''
    a = meas[0]
    d = meas[1]
    x = d*math.cos(math.radians(a))
    y = d*math.sin(math.radians(a))
    return (x,y)

def calc_gap(xy1,xy2):
    '''
    Given two points represented by (x,y) tuples, 
    calculate the distance between the two points.
    dist is the hyp of the triangle.
    
    dist = sqrt((x1-x2)^2 + (y1-y2)^2)
    '''
    dist = math.hypot(xy1[0]-xy2[0],xy1[1]-xy2[1])
    return dist

if __name__ == '__main__':
    main()
