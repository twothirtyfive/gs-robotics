from gopigo import *
from random import randint
import sys, time

counter = 0
SLP = 0.5

while (counter < 41):
    num = randint(0,5)
    print num
    if num == 0:
        fwd()
        time.sleep(SLP)
        stop()
        counter += 1
    elif num == 1:
        bwd()
        time.sleep(SLP)
        stop()
        counter += 1
    elif num == 2:
        left()
        time.sleep(SLP)
        stop()
        counter += 1
    elif num == 3:
        right()
        time.sleep(SLP)
        stop()
        counter += 1
    elif num == 4:
        servo(45)
        time.sleep(SLP)
        servo(135)
        time.sleep(SLP)
        servo(90)
        time.sleep(SLP)
        counter += 3
