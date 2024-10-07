# PyCraft
## nc file generation for stepcraft cnc in python


### Welcome!

This python repository allows for quick and easy (sort of...) nc file generation! Although its capabilities
are limited compared to Fusion 360, there are some advantages. First of all, for very simple parts, the process
is much quicker than fusion, and certain aspects are easier to customize. Additionally, fusion sometimes takes
a while to load and can be very frustrating! Here is a brief overview of how to use this tool.

#### 1) Identify the operations needed to cut the part.

Most parts require a few holes to be drilled in them (HolePaths), maybe some bearing holes too (paths), and then
a final path to do the outer contour of the part. Take note of what operations will be needed, these will be used in step 2.

#### 2) Set up the operations in user.py (and possibly scripts.py)

Next, you should enter the operations into user.py in the correct format. For simple shapes such as rectangles or ellipses,
you can use the Rectangle and Ellipse classes to create these paths. For holes that just require z-axis movement and a standard
drillbit, you can use HolePath. Finally, for more complex paths, follow these steps:
1) Load your path in onshape and take a screenshot. Save the screenshot to this directory.
2) Enter the path using the Contour class, with the input being the file name of the screenshot.

#### 3) Generate the gcode

Finally, generate the gcode by running the run.py python file. You should use the following command:

python3 run.py filename.nc

You should replace 'filename.nc' with whatever file name you want the generated nc program to have


##### That process was brief, and is certainly not enough to begin generating nc programs.\nIn order to better understand, you should watch tutorial.mp4, which displays the full process of \nsetting up and generating nc code for a part. You may also want to take a look at NC\_SETTINGS\_MANUAL.txt or PATH\_MANUAL.txt for specific information. The vast majority of 
