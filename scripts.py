# This file contains all functions that can be used in user.py for more complex stuff like iterating through a hole pattern.

import numpy as np
from paths import *

# Returns a list of the coordinates of a pattern of holes of xNum by yNum, with a gap of xGap and yGap in the x and y directions respectively.
def linearPattern(xNum, yNum, xGap, yGap, pos):
    res = []
    for y in range(yNum):
        for x in range(xNum):
            res.append((pos[0] + x*xGap, pos[1] + y*yGap))
    return res

def circularPattern(num, rad, pos, startAngle=0):
    res = []
    inc = 2*np.pi / num
    for i in range(num):
        curAngle = startAngle + i*inc
        res.append((pos[0] + rad*np.cos(curAngle), pos[1] + rad*np.sin(curAngle)))
    return res

