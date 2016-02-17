import ujson
from math import sqrt
grid = {}
f = open("geogrid.txt", "rb")
grid = ujson.load(f)
f.close()
geohash = {}
print len(grid)


def digit(num, dig):
    pos = str(num).rfind(".")
    if pos == -1:
        return None
    elif (len(str(num)) - 1 - pos) < dig:
        return None
    return int(str(num)[pos+dig])


def nestgen(nest, crd, counter):
    tempnest = geohash[temp][temp2]
    for x in range(len(nest)):
        if nest[x] in tempnest:
            if x == 0 and nest[x] == temp2:
                if len(nest) == 1:
                    counter +=1
                    tempnest.update({nest[x]: u"*|"})
                    continue
                tempnest.update({nest[x]: {}})
                tempnest = tempnest.get(nest[x])
            elif nest[x-1] == nest[x] and len(nest) != 1:
                tempnest.update({nest[x]: {}})
                tempnest = tempnest.get(nest[x])
            else:
                tempnest = tempnest.get(nest[x])
        elif x == len(nest)-1 or len(nest) == 1:
            counter+=1
            tempnest.update({nest[x]: u"*|"})
        else:
            tempnest.update({nest[x]: {}})
            tempnest = tempnest.get(nest[x])
    return counter


def fetch(coords):
    temp4 = geohash[(int(coords[0]) / 10, int(coords[1]) / 10)]
    temp4 = temp4[(int(coords[0]) % 10, int(coords[1]) % 10)]
    temp5 = pop_dec(coords)
    for z in temp5:
        if z in temp4:
            temp4 = temp4.get(z)
            continue
        elif temp4 == u"*|":
            return temp4
        else:
            return None
    return temp4


def pop_dec(inp, n=6):
    t = []
    for y in range(1, n):
        if type(digit(inp[0], y)) == int and type(digit(inp[1], y)) == int:
            t.append((digit(inp[0], y), digit(inp[1], y)))
        elif type(digit(inp[0], y)) == int and digit(inp[1], y) == None:
            t.append((digit(inp[0], y), 0))
        elif type(digit(inp[1], y)) == int and digit(inp[0], y) == None:
            t.append((0, digit(inp[1], y)))
        else:
            t.append((0,0))
    return t

counter = 0
for x in grid:
    x = [float(z) for z in x.lstrip("(").rstrip(")").split(",")]
    if (x[0]**2 + x[1]**2)**1/2 < 10:
        print x
    x = [round(x[0],6),round(x[1],6)]
    temp = (int(x[0]) / 10, int(x[1]) / 10)

    if temp not in geohash:
        geohash[temp] = {}
    temp2 = (int(x[0]) % 10, int(x[1]) % 10)
    if temp2 not in geohash[temp]:
        geohash[temp][temp2] = {}

    temp3 = pop_dec(x)

    counter = nestgen(temp3, x, counter)
    if not fetch(x):
        print x
        break

print counter
f = open("geogrid2.txt", "wb")
ujson.dump(geohash, f, ensure_ascii=False)
f.close()

