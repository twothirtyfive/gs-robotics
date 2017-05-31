from gopigo import *
from control import *
import math
import time

STOP_DIST=20 # Dist, in cm, before an obstacle to stop.
SAMPLES=4 # Number of sample readings to take for each reading.
INF=150 # Distance, in cm, to be considered infinity.
REPEAT=2
DELAY=.02

def main():
    print "*** Starting Find Hole Example ***"
    servo(1)
    time.sleep(0.2)

    angle_diff = findobstacle()
    print "Angle: {}".format(angle_diff)
    servo(90)
    stop()
    exit()

def findobstacle(increment):
	ret = []
    inc = 5
    print "Scanning room in {} degree increments".format(inc)
    for ang in range(40,140,inc):
        print "  Setting angle to {} ... ".format(ang),
        servo(ang)
        buf=[]
        for i in range(SAMPLES):
            dist=us_dist(15)
            print dist,
            if dist<140 and dist>=0:
                buf.append(dist)
            else:
                buf.append(INF)
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

# def scan_room():
#     ret = []
#     inc = int(math.degrees(math.atan(CHASS_WID/20)))
#     inc = int(inc/2)
#     print "Scanning room in {} degree increments".format(inc)
#     for ang in range(0,180,inc):
#         print "  Setting angle to {} ... ".format(ang),
#         ## resetting ang because I've seen issues with 0 and 180
#         if ang == 0: ang = 1
#         if ang == 180: ang = 179
#         servo(ang)
#         buf=[]
#         for i in range(SAMPLES):
#             dist=us_dist(15)
#             print dist,
#             if dist<140 and dist>=0:
#                 buf.append(dist)
#             else:
#                 buf.append(INF)
#         print
#         ave = math.fsum(buf)/len(buf)
#         print "  dist={}".format(ave)
#         ret.append((ang,ave))
#         ## Still having issues with inconsistent readings.
#         ## e.g. 
#         ##  Setting angle to   0 ...    18   19 218 49
#         ##  Setting angle to 170 ...  1000 1000  45 46
#         time.sleep(DELAY)
#     ## Reset servo to face front
#     servo(90)
#     return ret

# def findholes(readings):
    
#     print "Processing readings to find obstacles...."
#     print readings
#     holes = []
#     buf = []
#     ## Previous non-INF reading
#     prev = ()
#     for (a,d) in readings:
#         print "  {}:{}".format(a,d)
#         if d < INF:
#             ## If dist is not INF, then we've hit another
#             ## obstacle, so reset the buffer.
#             if len(buf) > 2:
#                 ## If the buffer has at least 3 INF readings,
#                 ## then record the hole.
#                 holes.append(buf)
#                 print "    Found a hole: {}:{}".format(a,d)
#             buf = []
#             continue
#         ## Add reading to buffer
#         buf.append((a,d))
#     ## In case the last reading was INF
#     if len(buf) > 2:
#         holes.append(buf)
#         print "    Found a hole: {}:{}".format(a,d)
#     return holes

