

# In the line below, replace Contour with whatever path you want to create (Contour, HolePath, Rectangle, Ellipse).
# Then, enter the correct settings within the parentheses that follow. The settings will defer for different types of paths, so check
# PATH_MANUAL.txt for more information.
Contour('images/exampleScreenshots/weirdShape.png', 100, 100, (0,0))

# In the line below, choose the settings for the machine. These settings will be used to generate the nc program. Don't break a bit!
# If you are unsure how to use these settings, take a look at NC_SETTINGS_MANUAL.txt for more information.
partDepth=6.35, retractHeight=10, bitOut=True, bitDiam=5, feedRate=100, plungeRate=20, spindleSpeed=1000, passes=6, spiral=True

# You should repeat these lines for as many paths that you want. All empty lines and lines that start with '#' will be ignored. 
# Make sure the line with the machine settings always comes after the path declaration line.
# For an example file, check demoFile.py. If you have any questions, contact me at lsitaraman677@student.fuhsd.org or ask me at robotics.

