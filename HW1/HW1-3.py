from gopigo import *
from control import *
import time

CRCM = 2 * 3.14159 * 3.25 ##approx 20.42cm
SLP = 0.3
dlist = []

def enc_move(tgt_dist):
    enc_num = (tgt_dist/CRCM) * 18
    return enc_num

def take_US():
    servo(90) ##set US sensor straight forward
    for x in range(0,5):
        dist = us_dist(15) ##find distance, 15 is connection to port A1
        dlist.append(dist)
        print "Distance: %s" %dist
        time.sleep(SLP)
    tdist = sum(dlist)/5.0 ##find average distance
    print "Averaged distance: %s" %tdist
    del dlist[:]

def move_gpg_bwd(mov_dist):
    mov = enc_move(mov_dist)
    enc_tgt(1,1, int(mov))
    bwd()
    time.sleep(SLP)


##5cm test from wall
take_US()

##move to 30cm from wall
move_gpg_bwd(25)

##30cm test from wall
take_US()

##move to 60cm from wall
move_gpg_bwd(30)

##60cm test from wall
take_US()
