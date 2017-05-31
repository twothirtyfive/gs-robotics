from gopigo import *
from control import *
import time

#should perform 360 turn
set_speed(100)
enc_tgt(0,1, 32)
bwd()
enc_tgt(1,0, 32)
fwd()
