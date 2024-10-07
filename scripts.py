# This file contains all functions that can be used in user.py for more complex stuff like iterating through a hole pattern.

# Returns a list of the coordinates of a pattern of holes of xNum by yNum, with a gap of xGap and yGap in the x and y directions respectively.
def holePattern(xNum, yNum, xGap, yGap, pos):
    res = []
    for y in range(yNum):
        for x in range(xNum):
            res.append((pos[0] + x*xGap, pos[1] + y*yGap))
    return res
