# This file is an example of how a file used by run.py to create an nc program might look!

# First path: Contour:
Contour('images/exampleScreenshots/demoPart.png', 100, 100, (0, 0))
partDepth=6.35, retractHeight=10, bitOut=True, bitDiam=6, feedRate=100, plungeRate=20, spindleSpeed=5000, passes=3, spiral=True

# Second path: Ellipse:
Ellipse(90, 90, (100, 0))
partDepth=6.35, retractHeight=10, bitOut=True, bitDiam=6, feedRate=100, plungeRate=20, spindleSpeed=5000, passes=3, spiral=True

# Third path: Rectangle:
Rectangle(90, 90, (0, 110))
partDepth=6.35, retractHeight=10, bitOut=True, bitDiam=6, feedRate=100, plungeRate=20, spindleSpeed=5000, passes=3, spiral=True

# Fourth path: HolePath:
HolePath([(0, 0), (-40, 0), (40, 0), (0, 40), (0, -40)], offset=(150, 150))
retractHeight=10, plungeRate=20, spindleSpeed=5000

# Fifth path: HolePath:
HolePath(linearPattern(xNum=6, yNum=6, xGap=10, yGap=10, pos=(200, 200)))
retractHeight=10, plungeRate=20, spindleSpeed=5000
