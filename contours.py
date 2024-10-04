import numpy as np
from PIL import Image

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


    def copy(self):
        res = contour(None, None, None, None)
        res.xVals = self.xVals
        res.yVals = self.yVals
        res.pos = self.pos
        return res

    def scale(self, kx, ky):
        self.xVals = (self.xVals - self.pos[0])*kx + self.pos[0]
        self.yVals = (self.yVals - self.pos[1])*ky + self.pos[1]

    def setCenter(self, newX, newY):
        self.xVals += newX - self.pos[0]
        self.yVals += newY - self.pos[1]
        pos = (newX, newY)
        

    def setRelativeReference(self, rx, ry):
        self.xVals += rx
        self.yVals += ry

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

    def setWidth(self, w):
        curWidth = (np.max(self.xVals) - np.min(self.xVals))
        self.scale(w / curWidth, 1)

    def setHeight(self, h):
        curHeight = (np.max(self.yVals) - np.min(self.yVals))
        self.scale(1, h / curHeight)



