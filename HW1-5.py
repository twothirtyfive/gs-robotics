from gopigo import *
from control import *
import time, math

#speed range from 0-255, default 200
set_speed(50)

def angle_finder(input):
    if input == []:
        return -1
    angles = []
    print input
    for a, b in input:
        print b
        angles.append(b)
    print angles
    min_angle = min(angles)
    max_angle = max(angles)
    angle = (min_angle + max_angle)/2.0
    print angle
    return angle

def avg_us_dist():
    dlist = []
    for x in range(0,3):
        dist = us_dist(15)
        dlist.append(dist)
    avg = sum(dlist)/len(dlist)
    return avg

def us_search(type):

    #rough search
    if type == 0:
        dlist = []
        ndlist = []
        for count in range (0,4):
            for x in range (0,12):
                angle = 15 * x
                if angle == 0:
                    angle = 1
                if angle == 180:
                    angle = 179
                servo(angle)
                time.sleep(0.15)
                dist = avg_us_dist()
                dlist.append((dist, angle + (count * 90)))
            turn('left', 90)
        print dlist
        for a, b in dlist:
            if 80 <= a <= 120:
                ndlist.append((a,b))
        print ndlist
        return ndlist

    #fine search
    if type == 1:
        y = 0
        tmplist = []
        alist = []
        for x in range(0, 18):
            angle = 45 + (5*x)
            servo(angle)
            time.sleep(0.15)
            temp = avg_us_dist()
            tmplist.append((temp, angle))
        for a, b in tmplist:
                if 80 <= a <= 120:
                    alist.append((a, b))
        return angle_finder(alist)

    #quick rough search
    if type == 2:
        dlist = []
        alist = []
        for x in range (0,12):
            angle = 15 * x
            if angle == 0:
                angle = 1
            if angle == 180:
                angle = 179
            servo(angle)
            time.sleep(0.15)
            dist = avg_us_dist()
            dlist.append((dist, angle))
        for a, b in dlist:
            if a <= 120:
                alist.append((a, b))
        return angle_finder(alist)
def corrected_turn(angle):
    if angle <= 90:
        turn('right', 90 - angle)
    if angle >= 270:
        turn('right', angle - 90)
    else:
        turn('left', angle - 90)


def main():
    object_list = us_search(0)
    angle = angle_finder(object_list)
    print angle
    corrected_turn(angle)
    angle = us_search(2)
    while angle == -1:
        turn('left', 45)
        angle = us_search(2)
    corrected_turn(angle)
    angle = us_search(1)
    print angle
    corrected_turn(angle)
    move_until(20)


main()
