import matplotlib.pyplot as plt
import math, sys#, control, gopigo
from time import sleep


CRCM = 2 * 3.14159 * 3.25
BIGNUM = 999999
OBS_DIST = 20

mov_table = []
obs_table = []
start = (0,0)
goal = (0,3)

#initate
def start_plot(start, goal):
    plt.plot(start)
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
            if orientation is <= 270:
                turn('right',orientation+90)
                temp = 90
                n = 1
            else:
                turn('left',(360-orientation)+90)
                temp = 90
                n = 2
        servo(temp)
        time.sleep(0.5)
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
            return 0
        elif distance <= OBS_DIST:  #return to previous orientation
            if n == 1:
                turn('left', orientation+90)
            elif n == 2:
                turn('right', (360-orientation)+90)
            return BIGNUM

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

start_plot(start, goal)
insert_mov_plot((0,2), 180)
insert_mov_plot((-1, 2), 90)
insert_mov_plot((-1, 3), 0)
insert_mov_plot((0,2), 90)
pos,orient = current_position()
#print "current position: {} {}".format(pos, orient)
#print_plots()
#plt.show()
