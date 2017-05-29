from gopigo import *
from control import *
import time

SLP = 0.3
dlist = []

def main():
  servo(90) ##set US sensor straight forward
  for x in range(0,3):
    dist = us_dist(15) ##find distance, 15 is connection to port A1
    dlist.append(dist)
    print dist
    time.sleep(SLP)
  tdist = sum(dlist)/3.0 ##find average distance
  print "Averaged distance: %s" %tdist
