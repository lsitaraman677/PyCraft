from paths import *
from matplotlib import pyplot as plt


pos = (0, 0)
w = 13.939 * 25.4
h = 7.234 * 25.4
a = Contour('images/demoPart.png', w, h, pos)
#a = Ellipse(w, h, pos)
#a = Rectangle(w, h, pos)

plt.plot(a.xVals, a.yVals)
plt.plot([pos[0], pos[0] + w, pos[0] + w, pos[0], pos[0]], [pos[1], pos[1], pos[1] + h, pos[1] + h, pos[1]])
plt.gca().axis('equal')
plt.show()
l = a.get_gcode(partDepth=6.35, retractHeight=10, bitOut=True, bitDiam=6, feedRate=100, plungeRate=20, spindleSpeed=5000, spiral=True)

with open('ncFiles/demoPart.nc', 'w') as f:
    lines = []
    lines.append('G17 G21 G90 G94\n')
    for i in l:
        lines.append(i + '\n')
    f.writelines(lines)

print('\ndone\n')
