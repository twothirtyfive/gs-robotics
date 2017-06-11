import matplotlib.pyplot as plt
import math, sys#, control, gopigo
from time import sleep


CRCM = 2 * 3.14159 * 3.25
mov_table = []
obs_table = []
start = (0,0)
goal = (0,3)

#initate
def start_plot(start, goal):
    plt.plot(start)
    mov_table.append(((0,0),90))

def test_plots():
    plt.plot(1,1)

#check plot for being previously visited
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
def find_current_plot(encoders, orientation):
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

    return ((nx,ny),orientation)

#insert obstacle plot
def insert_obs_plot(plot):
    x,y = plot
    plt.plot(x,y)
    obs_table.append(plot)

#return last known position
def current_position(mov_table):
    return mov_table[-1]


#print all plots
def print_plots():
    for n in range(0,len(plt.gca().get_lines())):
        print plt.gca().get_lines()[n].get_xydata()

start_plot(start, goal)
insert_mov_plot((0,2), 180)
insert_mov_plot((-1, 2), 90)
insert_mov_plot((-1, 3), 0)
insert_mov_plot((0,2), 90)
pos,orient = current_position(mov_table)
#print "current position: {} {}".format(pos, orient)
#print_plots()
#plt.show()
