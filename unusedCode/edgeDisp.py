from PIL import Image
from matplotlib import pyplot as plt
import numpy as np

curImage = Image.open('weirdShape.png', 'r')

data = list(curImage.getdata())
width, height = curImage.size

print(width, height)

getPixel = lambda x, y: data[(height-y-1)*width + x][:3]

centerX = None
centerY = None
step = 10
broken = False
for y in range(height):
    for x in range(width):
        if sum(getPixel(x, y)) < 760:
            centerX = x
            centerY = y
            broken = True
            break
    if broken == True:
        break

print(centerX, centerY)
theta = np.pi * 1.5
thetaStep = (np.pi / 180.0)*5
x = []
y = []
dist = 100*step
while dist > (step*0.75):
    x.append(centerX)
    y.append(centerY)
    curX = round(np.cos(theta)*step + centerX)
    curY = round(np.sin(theta)*step + centerY)
    while(sum(getPixel(curX, curY)) > 760):
        theta += thetaStep
        #print(f'tried ({curX}, {curY}). Did not work')
        curX = round(np.cos(theta)*step + centerX)
        curY = round(np.sin(theta)*step + centerY)
    #print('new coordinate is:', curX, curY)

    dist = ((curX - x[0])**2 + (curY - y[0])**2)**0.5
    centerX = curX
    centerY = curY
    theta += np.pi + np.pi/2

x.append(x[0])
y.append(y[0])

plt.plot(x, y)
plt.gca().axis('equal')
plt.show()





