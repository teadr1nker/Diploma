#!/usr/bin/python3
from bugs import *

ox, oy = [], []

sx = 0.0
sy = 0.0
gx = 160.0
gy = 105.0

addObstacle(20, 20, 20, 20, ox, oy)
addObstacle(60, 40, 40, 40, ox, oy)
addObstacle(120, 80, 20, 20, ox, oy)
addObstacle(80, 0, 60, 20, ox, oy)
addObstacle(0, 60, 20, 40, ox, oy)
addObstacle(20, 80, 20, 20, ox, oy)
addObstacle(120, 40, 40, 20, ox, oy)

bug = BugPlanner(sx, sy, gx, gy, ox, oy)
bug.bug1()
