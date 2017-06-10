import matplotlib.pyplot as plt
#import control, gopigo
from time import sleep

mov_table = []
obs_table = []
start = (0,0)
goal = (0,3)

#initate
def start_plot(start, goal):
    plt.plot(start,goal)
    mov_table.append(((0,0),90))

def test_plots():
    plt.plot(1,1)

#insert move plot
def insert_mov_plot(plot, orientation):
    x,y = plot
    plt.plot(x,y)
    mov_table.append(((plot),orientation))

#insert obstacle plot
def insert_obs_plot(plot):
    x,y = plot
    plt.plot(x,y)
    obs_table.append(plot)

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
pos,orient = current_position(mov_table)
print "current position: {} {}".format(pos, orient)
print_plots()
