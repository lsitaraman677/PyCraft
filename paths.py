import numpy as np
from PIL import Image

# Represents a general contour, generated from a screenshot
class Contour:

    def __init__(self, filename, width_in, height_in, position, reference=(0, 0), thetaStep=0.08727, step=10):
        
        #### Create default instance if any inputs are None ####
        if (filename is None):
            self.xVals = None
            self.yVals = None
            self.pos = None
            return

        #### Find the outer edge of the contour screenshot ####

        ## Setup ##

        # Load the image using PIL.Image
        curImage = Image.open(filename, 'r')
        # Get the data into a list
        data = list(curImage.getdata())
        # Get the width and height of the image
        width, height = curImage.size
        print(f'image succesfully loaded! Size: {width} x {height}')
        # Define a lambda to convert an x, y coordinate (x is right, y is up) to the (r,g,b,o) values at that point
        getPixel = lambda x, y: data[(height-y-1)*width + x][:3]
        
        ## Find the starting point ##

        # Initialize variables
        centerX = None
        centerY = None
        broken = False

        # Search verticaly from the bottom to find the lowest y-value point and initialize the starting values to that point
        for y in range(height):
            for x in range(width):
                # If the pixel isn't white, it is on the contour and is the starting location
                if sum(getPixel(x, y)) < 760:
                    centerX = x
                    centerY = y
                    broken = True
                    break
            if broken == True:
                break

        ## Trace out the outside edge of the part and store the values ##

        # Initialize x and y arrays and theta value
        theta = np.pi * 1.5
        x = []
        y = []
        # Make sure dist is larger than step
        dist = step + 1

        ## The following loop traces the outer edge of the contour by rotating a segment of length step 
        ## and checking when it contacts the part. It's basically rolling a ball around the part to
        ## track the contours and store them in x and y

        # Loop until dist is less than 0.75*step (the start point has connected back to the end point): 
        print('beginning path generation...')
        while dist > (step*0.75):
            # Add the current location to the arrays
            x.append(centerX)
            y.append(centerY)
            # Calculate the point to check based on theta, step, and the current location
            curX = round(np.cos(theta)*step + centerX)
            curY = round(np.sin(theta)*step + centerY)
            # While the current point to check isn't on the part's edge:
            while(sum(getPixel(curX, curY)) > 760):
                # Increment theta (counterclockwise)
                theta += thetaStep
                curX = round(np.cos(theta)*step + centerX)
                curY = round(np.sin(theta)*step + centerY)
            # Once the next point has been found, calculate the distance to see if the end has been reached    
            dist = ((curX - x[0])**2 + (curY - y[0])**2)**0.5
            # Update the current center
            centerX = curX * 1.0
            centerY = curY * 1.0

            # Update theta
            theta += np.pi + np.pi/2

        # Complete the loop by adding the first point onto the end
        x.append(x[0])
        y.append(y[0])

        # Initialize the members self.xVals and self.yVals
        self.xVals = np.array(x)
        self.yVals = np.array(y)
        print('part contour identified! Scaling contour values...')

        #### Modify the values to match the expected center and scale ####

        ## Scale ##

        # If the height or the width is None, calculated it appropriately for scale = 1:1
        w = 0
        h = 0
        if width_in is None:
            w = height_in * width / height
            h = height_in
        elif height_in is None:
            h = width_in * height / width
            w = width_in
        else:
            w = width_in
            h = height_in
        # Get bounding values:
        xMax = np.max(self.xVals)
        xMin = np.min(self.xVals)
        yMax = np.max(self.yVals)
        yMin = np.min(self.yVals)
        # Translate coordinates so that (0, 0) is the bottom-left corner of the bounding box
        self.xVals -= xMin
        self.yVals -= yMin
        # Calculate scale coefficients
        xScale = w / (xMax - xMin)
        yScale = h / (yMax - yMin)
        # Scale values
        self.xVals *= xScale
        self.yVals *= yScale
        
        ## Translate ##
        
        # Set the position
        self.pos = position
        # Translate values
        self.xVals += position[0] - reference[0]
        self.yVals += position[1] - reference[1]
        print('Scaling complete! Contour generated. Bounding rectangle (left x, bottom y, width, height): ', end='')
        print(f'{(position[0] - reference[0], position[1] - reference[1], w, h)}')

    # Return a contour object that is a copy of self
    def copy(self):
        res = contour(None, None, None, None)
        res.xVals = self.xVals
        res.yVals = self.yVals
        res.pos = self.pos
        return res

    # Scale in x and y
    def scale(self, kx, ky):
        self.xVals = (self.xVals - self.pos[0])*kx + self.pos[0]
        self.yVals = (self.yVals - self.pos[1])*ky + self.pos[1]

    # Set the center of the part (defined by reference)
    def setCenter(self, newX, newY):
        self.xVals += newX - self.pos[0]
        self.yVals += newY - self.pos[1]
        pos = (newX, newY)
        
    # Set the reference for the part relative to the current reference
    def setRelativeReference(self, rx, ry):
        self.xVals += rx
        self.yVals += ry

    # Set the reference for the part from the bottom left corner
    def setAbsoluteReference(self, rx, ry):
        # Get min values:
        xMin = np.min(self.xVals)
        yMin = np.min(self.yVals)
        # Find amounts to shift by
        diffX = pos[0] - xMin
        diffY = pos[1] - yMin
        shiftX = rx - diffX
        shiftY = ry - diffY
        # Shift the coordinates
        self.xVals += shiftX
        self.yVals += shiftY

    # Set the width of the part to a specified amount
    def setWidth(self, w):
        curWidth = (np.max(self.xVals) - np.min(self.xVals))
        self.scale(w / curWidth, 1)

    # Set the height of the part to a specified amount
    def setHeight(self, h):
        curHeight = (np.max(self.yVals) - np.min(self.yVals))
        self.scale(1, h / curHeight)

    # Helper method for get_gcode
    def getOffsetPoint(self, idx, bitDiam, inFact):
        points = len(self.xVals)
        curX = self.xVals[idx]
        curY = self.yVals[idx]
        nextIdx = np.mod((idx+3), points)
        prevIdx = np.mod((idx-3), points)
        dx = self.xVals[nextIdx] - self.xVals[prevIdx]
        dy = self.yVals[nextIdx] - self.yVals[prevIdx]
        normFact = bitDiam / ((dx**2 + dy**2)**0.5)
        curX += dy * normFact * inFact
        curY += -dx * normFact * inFact
        return curX, curY

    # Get an array of strings representing the lines of gcode to follow the contour
    def get_gcode(self, partDepth, retractHeight, bitDiam, bitOut, feedRate, plungeRate, spindleSpeed, passes=1, direction=1, finalPassDepth=0, extraDepth=0.05, spiral=False):

        depth_per_pass = (partDepth + extraDepth - finalPassDepth) / passes
        points = len(self.xVals)
        inFact = 1 if bitOut else -1
        startX, startY = self.getOffsetPoint(0, bitDiam, inFact)
        lines = [f'M{3 if (direction==1) else 4} S{spindleSpeed}', f'G0 X{startX} Y{startY} Z{retractHeight}']
        curZ = None 
        if spiral:
            curZ = (lambda p, i: partDepth - depth_per_pass*p - depth_per_pass*i/points) 
        else:
            curZ = (lambda p, i: partDepth - depth_per_pass*(p+1))

        for passNum in range(passes):
            for i in range(points):
                curX, curY = self.getOffsetPoint(i, bitDiam, inFact)
                curLine = f'G1 X{curX} Y{curY} Z{curZ(passNum, i)}'
                F = ''
                if(spiral):   
                    if(passNum == 0):
                        if(i == 0):     F = f' F{plungeRate}'
                        elif(i == 1):   F = f' F{feedRate}'
                else:
                    if(i == 0):         F = f' F{plungeRate}'
                    elif(i == 1):       F = f' F{feedRate}'
                curLine += F
                lines.append(curLine)

        if spiral or (finalPassDepth > 0):
            lines.append(f'G1 X{startX} Y{startY} Z{-extraDepth} F{plungeRate}')
            for i in range(1, points):
                curX, curY = self.getOffsetPoint(i, bitDiam, inFact)
                curLine = f'G1 X{curX} Y{curY}' + (f' F{feedRate}' if (i==1) else '')
                lines.append(curLine)

        lines.append(f'G0 X{startX} Y{startY} Z{retractHeight}')

        return lines
    
# An elliptical path. Inherits Contour.
class Ellipse(Contour):

    def __init__(self, w, h, position, thetaStep=0.08727):
        # Set the position
        self.pos = position

        # Set up for loop
        theta = 0
        xv = []
        yv = []
        x = position[0] + w*0.5
        y = position[1] + h*0.5
        xRad = w*0.5
        yRad = h*0.5

        # Add points to xv and yv as theta goes from 0 to 2pi
        print('beginning path generation')
        while theta < (2*np.pi):
            xv.append(np.cos(theta)*xRad + x)
            yv.append(np.sin(theta)*yRad + y)
            theta += thetaStep
        
        xv.append(position[0] + w)
        yv.append(position[1] + yRad)

        # Set the members xVals and yVals
        self.xVals = np.array(xv)
        self.yVals = np.array(yv)

        print(f'path generated. Bounding rectangle (x, y, w, h): ({position[0]}, {position[1]}, {w}, {h})')

    # Prevent the call of setRelativeReference
    def setRelativeReference(self, a, b):
        return
    
    # Prevent the call of setAbsoluteReference
    def setAbsoluteReference(self, a, b):
        return

# A rectanglular path. Inherits Contour.
class Rectangle(Contour):

    def __init__(self, w, h, position, reference=(0, 0)):
        # Set xVals and yVals
        print('rect')
        self.xVals = np.array([position[0], position[0] + w, position[0] + w, position[0], position[0]])
        self.yVals = np.array([position[1], position[1], position[1] + h, position[1] + h, position[1]])
        self.pos = position
    
    def getOffsetPoint(self, idx, bitDiam, inFact):
        curX = None
        curY = None
        if (idx == 0) or (idx == 3) or (idx == 4):
            curX = self.xVals[idx] - bitDiam*inFact
        else:
            curX = self.xVals[idx] + bitDiam*inFact

        if (idx == 0) or (idx == 1) or (idx == 4):
            curY = self.yVals[idx] - bitDiam*inFact
        else:
            curY = self.yVals[idx] + bitDiam*inFact

        return curX, curY

        
    

class HolePath:

    def __init__(self, holeList, offset=(0, 0)):
        self.holes = [(i[0]+offset[0], i[1]+offset[1]) for i in holeList]
        self.xVals = np.array([i[0] for i in holeList])
        self.yVals = np.array([i[1] for i in holeList])
        print('holepath')

    def get_gcode(self, retractHeight, plungeRate, spindleSpeed, direction=1, extraDepth=0.05):
        lines = [f'M{3 if (direction==1) else 4} S{spindleSpeed}']
        for hole in self.holes:
            lines.append(f'G0 X{hole[0]} Y{hole[1]} Z{retractHeight}')
            lines.append(f'G1 X{hole[0]} Y{hole[1]} Z{-extraDepth} F{plungeRate}')
            lines.append(f'G0 X{hole[0]} Y{hole[1]} Z{retractHeight}')
        return lines


