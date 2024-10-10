from paths import *
from gcode import generate_nc_files
from scripts import *
import sys

pathStrings = []
settingStrings = []
filename = None
try:
    filename = sys.argv[2]
except:
    filename = 'user.py'

with open(filename, 'r') as user:
    lines = user.readlines()
    count = 0
    for i in lines:
        curLine = i.strip()
        if len(curLine) > 0:
            if curLine[0] != '#':
                count += 1
                if (count%2 == 1):
                    pathStrings.append(curLine)
                else:
                    settingStrings.append(curLine)

ncInfo = []
for i in range(count // 2):
    createObj = f'c = {pathStrings[i]}'
    createNC = f'lines = c.get_gcode({settingStrings[i]})'
    exec(createObj)
    exec(createNC)
    ncInfo.append([lines, c])

generate_nc_files(ncInfo, f'ncFiles/{sys.argv[1]}')



