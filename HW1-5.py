from gopigo import *
from control import *
from time import sleep
from math import ceil

#speed range from 0-255
set_speed(60)

def angle_finder(input):
    if input == []:
        return -1
    angles = []
    for a, b in input:
        angles.append(b)
    angles.sort()
    if len(angles) > 2:
        angles.pop(0)
        angles.pop(-1)
    angle = sum(angles)/len(angles)
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
                time.sleep(0.3)
                dist = avg_us_dist()
                corrected_angle = angle
                if angle + (count * 90) >= 360:
                    corrected_angle = angle + (count * 90) - 360
                dlist.append((dist, corrected_angle))
            turn('left', 90)
        print dlist
        for a, b in dlist:
            if a <= 120:
                print "angle: %s" %b
                print "distance: %s" %a
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
            time.sleep(0.3)
            temp = avg_us_dist()
            tmplist.append((temp, angle))
        for a, b in tmplist:
                if a <= 120:
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
            time.sleep(0.3)
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
    print "Commencing rough search."
    object_list = us_search(0)
    angle = angle_finder(object_list)
    print angle
    raw_input("next...")
    corrected_turn(angle)
    angle = us_search(2)
    if angle == -1:
        print "Object is not where it is expected to be. Commencing backup search method."
    while angle == -1:
        if(angle != -1):
            break
        print "angle is -1"
        turn('right', 90)
        angle = us_search(2)
    corrected_turn(angle)
    print "Commencing fine search."
    angle = us_search(1)
    corrected_turn(angle)
    print "Approaching target."
    move_until(20)

main()
