from gopigo import *
from control import *
import time, math

def us_search(type, min, max):
    dlist = []
    ndlist = []
    if type == 0:   ##rough search
        for count in range (0,4):
            for x in range (0,12):
                angle = 5 + (15 * x)
                servo(angle)
                time.sleep(0.3)
                dist = us_dist(15)
                dlist.append((dist, angle + (count * 90)))
            left_rot()
            time.sleep(0.6)
            stop()
        for d in dlist:
            if d[0] < 100:
                print (d[0], d[1])
                ndlist.append((d[0], d[1]))
        return ndlist
    if type == 1:   ##fine search
        y = 0
        for x in range(0, max_angle - min_angle + 30):
            tmplist = []
            angle = min_angle + x - 15
            servo(angle)
            time.sleep(1)
            for z in range(0,5):
                temp = us_dist(15)
                tmplist.append(temp)
            dist = sum(tmplist)/5.0
            dlist.append((dist, angle))
        for l in dlist:
            print l
        for d in dlist:
            if d[0] < 100 in dlist:
                ndlist.append((d[0], d[1]))
        avglist = [a[1] for a in ndlist]
        avg_angle = sum(avglist)/len(avglist)
        return avg_angle


object_list = us_search(0, 0, 0)
min_angle = min(int(obj[1]) for obj in object_list)
max_angle = max(int(obj[1]) for obj in object_list)
final_angle = us_search(1, min_angle, max_angle)
print final_angle
