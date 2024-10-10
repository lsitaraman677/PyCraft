from matplotlib import pyplot as plt

def generate_nc_files(contour_paths, basename):
    oldTypes = []
    for i in range(len(contour_paths)):
        path = contour_paths[i][0]
        curType = type(contour_paths[i][1]).__name__
        count = None
        for j in range(len(oldTypes)):
            if oldTypes[j][0] == curType:
                oldTypes[j][1] += 1
                count = oldTypes[j][1]
                break
        if count is None:
            oldTypes.append([curType, 1])
            count = 1

        with open(basename + f'_{curType}{count}', 'w') as f:
            lines = ['%\n', '(--- PyCraft generated nc program ---)\n', 'G17 G21 G90 G94\n']
            lines.append('\n')
            lines.append('\n')
            lines.append(f'(Operation: {curType}{count})\n')
            for line in path:
                lines.append(line + '\n')
            lines.append('\n')
            lines.append('\n')
            lines.append('M30\n')
            lines.append('%\n')
            f.writelines(lines)
        
        plt.plot(contour_paths[i][1].xVals, contour_paths[i][1].yVals)

    plt.gca().axis('equal')
    plt.title(basename)
    plt.show()

