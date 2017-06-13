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
set_left_speed(64)
compass = 0

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
        max_enc = intersect_mline()
        for ang in range(60,15,-15):
            c_servo(ang-15)
            time.sleep(0.3)
            d = dream_team_us_dist()
            c_servo(ang)
            time.sleep(0.3)
            h = dream_team_us_dist()
            currentD = h
            print "obstacle at 0: dist = ",d
            print "obstacle at 15: dist = ",h

        t_left, t_right = enc_read(0), enc_read(1)
        t_avg = int((t_left+t_right)/2.)
        t_avg = t_avg + max_enc

        enc_avg = 0
        fwd()
        while h-5<= currentD <= h+5 or enc_calc < t_avg:
            enc_calc = int((read_enc(0) + read_enc(1))/2.)
            time.sleep(0.2)
            currentD = dream_team_us_dist()
            time.sleep (0.2)
        stop()

        enc_left, enc_right = enc_read(0) - t_left, enc_read(1) - t_right
        enc_avg = int((enc_left + enc_right)/2.0)
        __, orient = mov_table[-1]
        insert_mov_plot(find_current_plot(enc_avg), orient)

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
        a = 7
        t_left, t_right = enc_read(0), enc_read(1)
        my_fwd(a)
        enc_left, enc_right = enc_read(0) - t_left, enc_read(1) - t_right
        enc_avg = int((enc_left + enc_right)/2.0)

        turn('right',90)
        orient -= 90
        if orient < 0:
            orient = 360 + orient
        insert_mov_plot(find_current_plot(enc_avg), orient)
        intersect_mline()


        my_fwd(10)
        ang = my_adjust()
        if orient+ang < 0:
            orient = 360 + orient
        insert_mov_plot(find_current_plot(15), orient + ang)

        global compass
        compass -= 90
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
        c_servo(ang)
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
    ## Reset c_servo to face front
    c_servo(90)
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





CRCM = 2 * 3.14159 * 3.25
BIGNUM = 999999
OBS_DIST = 20

mov_table = []
obs_table = []
goal = (0,3)

#initate
def start_plot():
    plt.plot(0,0)
    mov_table.append(((0,0),90))

#check plot for being previously visited, 0 means you've been there before
def check_plot(plot):
    cx,cy = plot
    print plot
    for pos,orient in mov_table:
        print pos
        x,y = pos
        if (x - .1 <= cx <= x + .1) and (y - .1 <= cy <= y + .1):
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
    distance = (encoders*CRCM)/18.
    pos,orient = mov_table[-1]
    var_x = 1.
    var_y = 1.
    x,y = pos
    if orient > 90:
        temp = orient
    elif 90 < orient <= 180:
        temp = 180 - orient
        var_x = -1.
    elif 180 < orient <= 270:
        temp = 270 - orient
        var_x = -1.
        var_y = -1.
    elif 270 < orient <= 360:
        temp = 360 - orient
        var_y = -1.

    ydist = var_y * distance * math.sin(math.radians(orient))
    xdist = var_x * distance * math.cos(math.radians(orient))

    nx = (xdist + x)/100.
    ny = (ydist + y)/100.

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
    plot,orientation = current_position()
    x,__ = plot
    if x >= 0 and 90 < orientation <= 270:
        if 90 < orientation <= 180:
            temp = 180 - orientation
        elif 180 < orientation <= 270:
            temp = 270 - orientation
    elif x < 0 and (0 <= orientation <= 90 or 270 < orientation <= 360):
        if 0 <= orientation <= 90:
            temp = orientation
        elif 270 < orientation <= 360:
            temp = 360 - orientation
    else:   #not oriented towards mline
        return BIGNUM

    dist = math.abs(x) / math.cos(math.radians(temp)) * 100 #convert m to cm

    #if at the mline
    if dist < 10:
        n = 0
        if 0 <= orientation <= 180:
            if orientation < 90:
                temp = 180 - orientation
        elif 180 < orientation <= 360:
            if orientation <= 270:
                turn('right',orientation+90)
                temp = 90
                n = 1
            else:
                turn('left',(360-orientation)+90)
                temp = 90
                n = 2
        c_servo(temp)
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
        elif distance <= OBS_DIST:  #return to previous orientation
            if n == 1:
                turn('left', orientation+90)
            elif n == 2:
                turn('right', (360-orientation)+90)
            return BIGNUM
        #if we are going to travel along the mline with a future obstacle
        else:
            pos,orient = mov_table[-1]
            x,y = pos
            if 0 <= orient <= 90:
                turn = 90 - orient
                turn('left', turn)
            elif 90 < orient <= 270:
                turn = orient - 90
                turn('right', turn)
            my_fwd(15)
            insert_mov_plot((x,y+0.15), 90)
            runner()

    #number of encoders to the closest mline point on current orientation
    return (dist/CRCM)*18.

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
    mov_dist = []
    inline = True
    abreast = False
    goal = 200
    toGoal = 0
    atGoal = False
    print "*** Starting BUG2 Example ***"
    c_servo(90)
    start_plot()
    runner()

def runner():
    d = dream_team_us_dist()
    d = d - 8
    start_left, start_right = enc_read(0), enc_read(1)
    my_fwd(d-5)

    mov_dist.append(d)

    toGoal += d
    delta_left_enc = enc_read(0) - start_left
    delta_right_enc = enc_read(1) - start_right
    ang = my_turn()

    __, orient = mov_table[-1]
    insert_mov_plot(find_current_plot(mov_dist[-1]), orient + ang)

    compass += ang
    inline = False
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
