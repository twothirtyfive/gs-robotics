#!/usr/bin/python
'''
This module contains convenience functions to simplify
the coding of simple tasks.
This really needs to be moved to a GoPiGo package
e.g. from gopigo.control import *
'''

from gopigo import *
from math import ceil
from time import sleep

en_debug=1

## 360 roation is ~64 encoder pulses or 5 deg/pulse
## DPR is the Deg:Pulse Ratio or the # of degrees per
##  encoder pulse.
DPR = 360.0/64
WHEEL_RAD = 3.25 # Wheels are ~6.5 cm diameter.
CHASS_WID = 13.5 # Chassis is ~13.5 cm wide.
VAR = 1.0

#left encoder, right encoder, # of encoders, fwd/bwd
def g_enc_tgt(direction, distance):
    x = 60
    set_speed(x)
    enc_tgt(1, 1, int((distance/(2*3.14159*WHEEL_RAD)) * 18))
    if direction == 'fwd':
        fwd()
    elif direction == 'bwd':
        bwd()
    else:
        print "invalid direction - no action"
    while read_enc_status() != 0:
        set_speed(x)
        time.sleep(x/120)
        if x < 210:
            x += 30

def turn(direction, degrees):
    #this function allows GPG to turn in place
    set_speed(80)
    conv_enc = (degrees/360.0) * 32.0
    if conv_enc <= 0:
        print "enc <= 0"
        conv_enc = 1
    if direction == 'left':
        enc_tgt(1, 1, int(math.ceil(conv_enc)))
        left_rot()
        time.sleep(conv_enc/5)
    elif direction == 'right':
        enc_tgt(1, 1, int(math.ceil(conv_enc)))
        right_rot()
        time.sleep(conv_enc/5)
    else:
        print "invalid direction"
        raise SystemExit
    return

def avg_us_dist():
    dlist = []
    for x in range(0,3):
        dist = us_dist(15)
        print dist
        dlist.append(dist)
        time.sleep(0.2)
    avg = sum(dlist)/len(dlist)
    return avg

def move_until(distance_away):
    servo(90)
    set_speed(150)
    while avg_us_dist() > (3 * distance_away):
        fwd()
        time.sleep(0.05)
    set_speed(75)
    while avg_us_dist() > distance_away:
        fwd()
        time.sleep(0.05)
    stop()
    return

def left_deg(deg=None):
    '''
    Turn chassis left by a specified number of degrees.
    DPR is the #deg/pulse (Deg:Pulse ratio)
    This function sets the encoder to the correct number
     of pulses and then invokes left().
    '''
    if deg is not None:
        pulse= int(deg/DPR)
        enc_tgt(0,1,pulse)
    left()

def right_deg(deg=None):
    '''
    Turn chassis right by a specified number of degrees.
    DPR is the #deg/pulse (Deg:Pulse ratio)
    This function sets the encoder to the correct number
     of pulses and then invokes right().
    '''
    if deg is not None:
        pulse= int(deg/DPR)
        enc_tgt(1,0,pulse)
    right()

def fwd_cm(dist=None):
    '''
    Move chassis fwd by a specified number of cm.
    This function sets the encoder to the correct number
     of pulses and then invokes fwd().
    '''
    if dist is not None:
        pulse = int(cm2pulse(dist))
        enc_tgt(1,1,pulse)
    fwd()

def bwd_cm(dist=None):
    '''
    Move chassis bwd by a specified number of cm.
    This function sets the encoder to the correct number
     of pulses and then invokes bwd().
    '''
    if dist is not None:
        pulse = int(cm2pulse(dist))
        enc_tgt(1,1,pulse)
    bwd()

def cm2pulse(dist):
    '''
    Calculate the number of pulses to move the chassis dist cm.
    pulses = dist * [pulses/revolution]/[dist/revolution]
    '''
    wheel_circ = 2*math.pi*WHEEL_RAD # [cm/rev] cm traveled per revolution of wheel
    revs = dist/wheel_circ
    PPR = 18 # [p/rev] encoder Pulses Per wheel Revolution
    pulses = PPR*revs # [p] encoder pulses required to move dist cm.
    if en_debug:
        print 'WHEEL_RAD',WHEEL_RAD
        print 'revs',revs
        print 'pulses',pulses
    return pulses
