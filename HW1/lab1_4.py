from gopigo import *
from control import *
import math
import time

STOP_DIST=20 # Dist, in cm, before an obstacle to stop.
SAMPLES=4 # Number of sample readings to take for each reading.
INF=150 # Distance, in cm, to be considered infinity.
REPEAT=2
DELAY=.2

def main():
    print "*** Starting Find Hole Example ***"
    servo(1)
    time.sleep(0.2)
    starting = findstarting()
    print "Starting Angle: {}".format(starting)
    diff = angle_diff(starting)
    print "Angle of Cone: {}".format(diff)
    servo(90)
    stop()
    exit()

def findstarting():
    ret = []
    inc = 5
    found = False
    starting = 0
    print "Scanning room in {} degree increments".format(inc)
    for ang in range(70,120,inc):
        print "  Setting angle to {} ... ".format(ang)
        servo(ang)
        buf=[]
        for i in range(SAMPLES):
            dist=us_dist(15)
            print dist
            if dist<100 and dist>=0:
                buf.append(dist)
            else:
                buf.append(INF)
        ave = math.fsum(buf)/len(buf)
        print "ave" + str(ave)

        if ave<100 and ave>=0:
            found = True
            starting = ang
            return starting

        time.sleep(DELAY)

def angle_diff(starting):
    shallow = True
    neg = True
    ang = starting
    mx = 0
    mn = 0
    while shallow:
        print "  Setting angle to {} ... ".format(ang)
        servo(ang)
        frame = False
        buf = []
        for i in range(SAMPLES):
            dist=us_dist(15)
            print dist
            if dist<100 and dist>=0:
                buf.append(dist)
            else:
                buf.append(INF)
        ave = math.fsum(buf)/len(buf)
        print "ave" + str(ave)

        if ave<100 and ave>=0:
            frame = True
            
        if frame:
            ang += 1
        else:
            shallow = False
            mx = ang - 1
            ang = starting - 1
        time.sleep(DELAY)
    while neg:
        print "  Setting angle to {} ... ".format(ang)
        servo(ang)
        frame = False
        buf = []
        for i in range(SAMPLES):
            dist=us_dist(15)
            print dist
            if dist<100 and dist>=0:
                buf.append(dist)
            else:
                buf.append(INF)
        ave = math.fsum(buf)/len(buf)
        print "ave" + str(ave)

        if ave<100 and ave>=0:
            frame = True
        if frame:
            ang -= 1
        else:
            neg = False
            mn = ang + 1
        time.sleep(DELAY)
    diff = mx-mn
    return diff



main()
