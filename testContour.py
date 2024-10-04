from contours import Contour
from matplotlib import pyplot as plt


pos = (100, 100)
w = 10
h = 20
a = Contour('thing2.png', w, h, pos)

plt.plot(a.xVals, a.yVals)
plt.plot([pos[0], pos[0] + w, pos[0] + w, pos[0], pos[0]], [pos[1], pos[1], pos[1] + h, pos[1] + h, pos[1]])
plt.gca().axis('equal')
plt.show()
