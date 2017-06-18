from gopigo import *
from control import *
from time import sleep
import math, sys
import matplotlib.pyplot as plt

STOP_DIST=20 # Dist, in cm, before an obstacle to stop.
SAMPLES=4 # Number of sample readings to take for each reading.
INF=200 # Distance, in cm, to be considered infinity.
REPEAT=2
DELAY=.02
set_speed(60)
# set_left_speed(66)
compass = 0
mov_dist = []
toGoal = 0
obstacleBegin = True

def my_fwd(dist):
    if dist is not None:
        pulse = int(cm2pulse(dist))
        enc_tgt(1,1,pulse)
        fwd()
        while read_enc_status() != 0:
            time.sleep(0.1)

def obstacle():
    abreast = True
    while abreast:
        print mov_table
        max_enc = intersect_mline()
        #goes through different values for debugging purposes
        for ang in range(60,15,-15):
            c_servo(ang)
            time.sleep(0.3)
            h = dream_team_us_dist()

            c_servo(ang-15)
            time.sleep(0.3)
            d = dream_team_us_dist()
            
            
            currentD = h
            print "obstacle at 0: dist = ",d
            print "obstacle at 15: dist = ",h

        t_left, t_right = enc_read(0), enc_read(1)
        print "tleft: ",t_left
        print "tright: ",t_right
        t_avg = t_left + t_right
        t_avg /= 2
        print "t_avg: ",t_avg
        if max_enc is not -1:
            t_avg = t_avg + max_enc
        print t_avg
        enc_avg = 0
        if t_avg > 1500:
            t_avg = 0
        fwd()
        enc_calc = int((enc_read(0) + enc_read(1))/2.)
        print enc_calc
        while (currentD <= h+20 and currentD <= d+20):
            if max_enc is not -1 and enc_calc >= t_avg:
                stop()
                
                enc_left, enc_right = enc_read(0) - t_left, enc_read(1) - t_right
                enc_avg = int((enc_left + enc_right)/2.0)
                __, orient = mov_table[-1]
                turn('left',90)
                orient += 90
                insert_mov_plot(find_current_plot(enc_avg), orient)

                intersect_mline()
                print "didn't happen"
                break
            enc_calc = int((enc_read(0) + enc_read(1))/2.)
            # time.sleep(0.2)

            prevD = currentD
            currentD = dream_team_us_dist()
            if currentD > prevD*2:
                print "temp CurrentD",currentD
                currentD = dream_team_us_dist()
            print "CurrentD",currentD
            # time.sleep (0.2)
        stop()

        if enc_calc >= t_avg:
            intersect_mline()

        # c_servo(90)
        time.sleep(0.2)
        currentD = dream_team_us_dist()
        time.sleep(0.2)
        operand = h*h - d*d
        # if operand > 0.0:
        #     a = math.sqrt(operand) + 7
        # else:
        a = 20
        t_left, t_right = enc_read(0), enc_read(1)
        my_fwd(a)
        enc_left, enc_right = enc_read(0) - t_left, enc_read(1) - t_right
        enc_avg = int((enc_left + enc_right)/2.0)
        __, orient = mov_table[-1]

        turn('right',100) #100 instead of 90 to account for error in machine
        orient -= 90
        if orient < 0:
            orient = 360 + orient
        insert_mov_plot(find_current_plot(enc_avg), orient)
        intersect_mline()


        my_fwd(25)
        # ang = my_adjust()
        # if orient+ang < 0:
        #     orient = 360 + orient
        insert_mov_plot(find_current_plot(15), orient)# + ang)

        global compass
        compass -= 90
        global obstacleBegin
        obstacleBegin = False
        # else:
        #     ang = my_turn()
        #     global compass
        #     compass += ang

def my_turn():
    c_servo(80)
    time.sleep(0.2)
    rdist = dream_team_us_dist()
    c_servo(90)
    time.sleep(0.2)
    mdist = dream_team_us_dist()
    c_servo(100)
    time.sleep(0.2)
    ldist = dream_team_us_dist()
    time.sleep(0.2)
    if ldist >= mdist or rdist >= mdist:
        deg = 90
    else:
        a = math.sqrt(ldist*ldist + rdist*rdist - 2.0*ldist*rdist*math.cos(math.radians(20)))
        beta = math.degrees(math.asin(ldist*math.sin(math.radians(20))/a))
        deg = 180-beta
    print "deg ",deg
    my_fwd(5)
    # deg += 10
    turn('left',deg)
    return deg

def my_adjust():
    c_servo(60)
    time.sleep(0.2)
    rdist = dream_team_us_dist()
    time.sleep(0.2)
    c_servo(75)
    time.sleep(0.2)
    ldist = dream_team_us_dist()
    time.sleep(0.2)
    a = math.sqrt(ldist*ldist + rdist*rdist - 2.0*ldist*rdist*math.cos(math.radians(15)))
    beta = math.degrees(math.asin(ldist*math.sin(math.radians(15))/a))
    deg = 150-beta
    if deg > 0:
        turn('right',deg)
    else:
        deg *= -1
        turn('left',deg)
        deg *= -1
    deg += 90
    return deg

def move(min_dist):
    ## Set c_servo to point straight ahead
    c_servo(90)
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



CRCM = 2 * 3.14159 * 3.25
BIGNUM = -1
OBS_DIST = 20

mov_table = []
obs_table = []
goal = (0,2.)

#initate
def start_plot():
    plt.plot(0,0)
    mov_table.append(((0,0),90))

#check plot for being previously visited, 0 means you've been there before
def check_plot(plot):
    cx,cy = plot
    for pos,orient in mov_table:
        x,y = pos
        if (x - .005 <= cx <= x + .005) and (y - .005 <= cy <= y + .005):
            return 0
    return 1

#check if at goal
def check_goal(plot):
    if plot == goal:
        print "Goal reached!"
        raise SystemExit

#insert move plot
def insert_mov_plot(plot, orientation):
    x,y = plot
    check_goal(plot)
    if check_plot(plot) == 1:   #verifies this location has not alreaedy been visited
        plt.plot(x,y)
        mov_table.append(((plot),orientation))
    else:
        print "bad! we have returned to a previously visited position"

#after moving and turning, returns current position and orientation (for adding to plots)
def find_current_plot(encoders):
    distance = math.fabs((encoders*CRCM)/18.) / 100.
    pos,orient = mov_table[-1]
    x,y = pos

    ydist = distance * math.sin(math.radians(orient))
    xdist = distance * math.cos(math.radians(orient))

    nx = xdist + x
    ny = ydist + y

    return (nx,ny)

#insert obstacle plot
def insert_obs_plot(plot):
    x,y = plot
    plt.plot(x,y)
    obs_table.append(plot)

#return last known position
def current_position():
    return mov_table[-1]

#use this after inserting the newest plot and adding to mov_table, returns distance(enc) to mline
def intersect_mline():
    BIGNUM = -1
    if not obstacleBegin:
        print "mline enter"
        print
        plot,orientation = current_position()
        x,__ = plot
        # if x >= 0 and 90 < orientation <= 270:
        #     if 90 < orientation <= 180:
        #         temp = 180 - orientation
        #     elif 180 < orientation <= 270:
        #         temp = 270 - orientation
        # elif x < 0 and (0 <= orientation <= 90 or 270 < orientation <= 360):
        #     if 0 <= orientation <= 90:
        #         temp = orientation
        #     elif 270 < orientation <= 360:
        #         temp = 360 - orientation
        # elif x >= 0 and (90 > orientation or orientation > 270):
        #     temp = orientation

        # else:   #not oriented towards mline
        #     print "return1"
        #     return BIGNUM

        dist = math.fabs(x) * 100 #convert m to cm
        print "dist: ",dist
        #if at the mline
        if dist < 5:
            n = 0
            temp = 0
            if 0 <= orientation <= 180:
                if orientation < 90:
                    temp = 90 - orientation
            elif 180 < orientation <= 360:
                if orientation <= 270:
                    turn('right',270-orientation)
                    temp = 90
                    n = 1
                else:
                    turn('left',(360-orientation)+90)
                    temp = 90
                    n = 2
            c_servo(temp + 90)
            time.sleep(.2)
            distance = dream_team_us_dist()
            goal_dist = distance_to_goal()

            #if you can see the goal unobstructed, go for it
            if distance >= goal_dist:
                enc = (goal_dist/CRCM) * 18.
                if 0 <= orientation <= 90:
                    turn('left', 90-orientation)
                elif 90 < orientation <= 180:
                    turn('right', orientation-90)
                enc_tgt(1,1, int(math.ceil(enc)))
                fwd()
                while read_enc_status() != 0:
                    time.sleep(.2)
                stop()
                print "Goal Reached!"
                raise SystemExit
            # elif distance <= OBS_DIST:  #return to previous orientation
            #     if n == 1:
            #         turn('left', orientation+90)
            #     elif n == 2:
            #         turn('right', (360-orientation)+90)
            #     print "return2"
            #     return BIGNUM
            #if we are going to travel along the mline with a future obstacle
            else:
                pos,orient = mov_table[-1]
                x,y = pos
                if 0 <= orient <= 90:
                    turn_deg = 90 - orient
                    turn('left', turn_deg)
                elif 90 < orient <= 270:
                    turn_deg = orient - 90
                    turn('right', turn_deg)
                my_fwd(15)
                insert_mov_plot((x,y+0.15), 90)
                print "return3"

                runner()

        #number of encoders to the closest mline point on current orientation
        print "return4"
        if orientation == 90:
            return BIGNUM
        print "dist: ",dist
        return dist

    return BIGNUM

#return distance in cm
def distance_to_goal():
    pos,orient = mov_table[-1]
    gx,gy = goal
    x,y = pos
    dist = math.sqrt((gx-x)*(gx-x) + (gy-y)*(gy-y))
    return dist*100 #convert m to cm

#print all plots
def print_plots():
    for n in range(0,len(plt.gca().get_lines())):
        print plt.gca().get_lines()[n].get_xydata()

def main():
    #mov_dist = []
    inline = True
    abreast = False
    # goal = 200
    global toGoal
    toGoal = 0
    atGoal = False
    print "*** Starting BUG2 Example ***"
    c_servo(90)
    start_plot()
    runner()

def runner():
    d = dream_team_us_dist()
    d = d - 5
    start_left, start_right = enc_read(0), enc_read(1)
    my_fwd(d-5)
    global mov_dist
    mov_dist.append(d)
    global toGoal
    toGoal += d
    delta_left_enc = enc_read(0) - start_left
    delta_right_enc = enc_read(1) - start_right
    ang = my_turn()

    __, orient = mov_table[-1]
    insert_mov_plot(find_current_plot(mov_dist[-1]), orient + ang)
    global compass
    compass += ang
    inline = False
    global obstacleBegin
    obstacleBegin = True
    obstacle()

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
    # c_servo(90)
if __name__ == '__main__':
    main()
