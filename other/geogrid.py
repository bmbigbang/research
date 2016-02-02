import csv
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import ujson

grid = {}; grid2={}
with open("urbanareas1_1.tsv", "rb") as csvfile:
    for i in csv.reader(csvfile, delimiter="\t"):
        if i[3]=="Latitude":
            continue
        grid[unicode(str(i[3])+","+str(i[4]))] = [i[0],i[2],i[6]]
    csvfile.close()
xstep = 360/100.0; tempgrid = {}

def gridder(x1,y1,step,div=3):
    step = step/div; ddense = False
    for i in np.arange(x1+step/2,x1+(step*div),step):
        for j in np.arange(y1+step/2,y1+(step*div),step):
            if step > xstep/100:
                for k in grid:
                    coords = [float(p) for p in k.split(",")]
                    if abs(i - coords[1]) < step/2 and abs(j - coords[0]) < step/2:
                        ddense = True;
                        gridder(i-(step/2),j-(step/2),step)
                        break
                if not ddense:
                    tempgrid[(i,j)] = step
                ddense = False
                continue
            tempgrid[(i,j)] = step
   
dense = False; x=-180.0; y=-90.0
while x < 179.99:
    while y < 89.99:
        for i in grid:
            coords = [float(p) for p in i.split(",")]
            if abs(x+(xstep/2) - coords[1]) < xstep/2 and abs(y+(xstep/2) - coords[0]) < xstep/2:
                gridder(x,y,xstep)
                grid2.update(tempgrid);tempgrid={}; dense = True; break
        if not dense:
            grid2[(x+(xstep/2),y+(xstep/2))] = xstep
        y+=xstep
        dense = False
    y=-90
    x+=xstep
            
x = []; y = []; z = []; zs = []; xs= []; ys =[]

for i in grid2:
    if grid2[i] not in z:
        z.append(grid2[i])
        x.append([])
        y.append([])
for i in grid2:
    x[z.index(grid2[i])].append(i[0])
    y[z.index(grid2[i])].append(i[1])
if ((len(z)-1)/4)+1 > 1:
    gs = gridspec.GridSpec(4,((len(z)-1)/4)+1)
else:
    gs = gridspec.GridSpec(len(z)%4,1)

gs.update(hspace=0.7)
for i in range(len(z)):
    plt.figure(1)
    plt.subplot(gs[(i%4),(i/4)])
    plt.scatter(x[i],y[i],c="r",marker=".")
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title("Step size: " + str(z[i]))

plt.figure(2)
for j in grid:
    for i in grid2:
        coords = [float(p) for p in j.split(",")]
        if abs(i[0] - coords[1]) < xstep and abs(i[1] - coords[0]) < xstep:
            xs.append(i[0])
            ys.append(i[1])
            zs.append(grid2[i])
    break

ax = plt.figure(2).add_subplot(111, projection='3d')
ax.scatter(xs, ys, zs, c='r',marker='o')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Step size')


plt.show()

f = open("geogrid.txt", "wb")
ujson.dump(grid2, f)
f.close()