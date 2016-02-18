import csv
import numpy as np
import json

grid = {}; grid2={}
with open("urbanareas1_1.tsv", "rb") as csvfile:
    for i in csv.reader(csvfile, delimiter="\t"):
        if i[3] == "Latitude":
            continue
        grid[unicode(str(i[3])+","+str(i[4]))] = [i[0],i[2],i[6]]
    csvfile.close()
xstep = 360/111.1; tempgrid = {}

def gridder(x1, y1, step, div=3):
    step = step/div; ddense = False
    for i in np.arange(x1 + step/2, x1 + (step*div), step):
        for j in np.arange(y1 + step/2, y1 + (step*div), step):
            if step > xstep/100:
                for k in grid:
                    coords = [float(p) for p in k.split(",")]
                    if abs(i - coords[1]) < step/2 and abs(j - coords[0]) < step/2:
                        ddense = True;
                        gridder(i-(step/2), j-(step/2), step)
                        break
                if not ddense:
                    tempgrid["({0[0]},{0[1]})".format((i, j))] = step
                ddense = False
                continue
            tempgrid["({0[0]},{0[1]})".format((i, j))] = step
   
dense = False; x = -180.0; y = -90.0
while x < 179.99:
    while y < 89.99:
        for i in grid:
            coords = [float(p) for p in i.split(",")]
            if abs(x+(xstep / 2) - coords[1]) < xstep / 2 and abs(y+(xstep / 2) - coords[0]) < xstep / 2:
                gridder(x, y, xstep)
                grid2.update(tempgrid); tempgrid={}; dense = True; break
        if not dense:
            grid2["({0[0]},{0[1]})".format((x+(xstep / 2), y+(xstep / 2)))] = xstep
        y += xstep
        dense = False
    y = -90
    x += xstep


f = open("geogrid.txt", "wb")
json.dump(grid2, f)
f.close()
