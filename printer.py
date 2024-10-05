from PIL import Image
from matplotlib import pyplot as plt

curImage = Image.open('weirdShape.png', 'r')

data = list(curImage.getdata())
width, height = curImage.size

xStep = 10
yStep = 20
x = []
y = []
print(width, height)
for i in range(0, height, yStep):
    for j in range(0, width, xStep):
        string = ''
        if sum(data[i*width + j][:-1]) < 760:
            string = '@'
            x.append(j)
            y.append(i)
        else:
            string = '.'
        print(string + ' '*(1 - len(string)), end='')
    print()

plt.scatter(x, y)
plt.gca().axis('equal')
plt.show()
