import json
from math import sqrt

class geogrid(dict):
    def __init__(self, grid):
        for coords in grid:
            coords_float = [float(z) for z in coords.lstrip("(").rstrip(")").split(",")]
            coords_float = [round(coords_float[0], 6), round(coords_float[1], 6)]
            coords = [z for z in coords.lstrip("(").rstrip(")").split(",")]
            geonest = self

            if coords_float[0] < 0.0:
                if "-" not in geonest:
                    geonest["-"] = {}
                geonest = geonest.get("-")
                coords_float[0] = abs(coords_float[0])
            else:
                if "+" not in geonest:
                    geonest["+"] = {}
                geonest = geonest.get("+")
            if coords_float[1] < 0.0:
                if "-" not in geonest:
                    geonest["-"] = {}
                coords_float[1] = abs(coords_float[1])
            else:
                if "+" not in geonest:
                    geonest["+"] = {}
                geonest = geonest.get("+")

            temp = [int(round(coords_float[0], -1))/10, int(round(coords_float[1], -1))/10]
            if temp[0] not in geonest:
                geonest[temp[0]] = {}
            geonest = geonest.get(temp[0])
            if temp[1] not in geonest:
                geonest[temp[1]] = {}
            geonest = geonest.get(temp[1])
            temp = [int(abs(coords_float[0])) % 10, int(abs(coords_float[1])) % 10]
            if temp[0] not in geonest:
                geonest[temp[0]] = {}
            geonest = geonest.get(temp[0])
            if temp[1] not in geonest:
                geonest[temp[1]] = {}
            geonest = geonest.get(temp[1])
            for y in range(6):
                if len(coords[0][coords[0].find("."):]) - (y + 2) < 0:
                    temp = 0
                else:
                    temp = int(coords[0][coords[0].find(".") + y + 1])
                if temp not in geonest:
                    geonest[temp] = {}
                geonest = geonest.get(temp)

                if len(coords[1][coords[1].find("."):]) - (y + 2) < 0:
                    temp = 0
                else:
                    temp = int(coords[1][coords[1].find(".") + y + 1])
                if temp not in geonest:
                    geonest[temp] = {}
                geonest = geonest.get(temp)
    def nearest(self, coords):
        coords_float = [float(z) for z in coords.split(",")]
        geonest = self
        res = ["", ""]

        if coords_float[0] < 0:
            geonest = geonest.get("-")
            coords_float[0] = abs(coords_float[0])
            res[0] += "-"
        else:
            geonest = geonest.get("+")
        if coords_float[1] < 0:
            geonest = geonest.get("-")
            coords_float[1] = abs(coords_float[1])
            res[0] += "-"
        else:
            geonest = geonest.get("+")


        if abs(coords_float[0]) < 10 and abs(coords_float[1]) > 10:
            temp = [0, int(round(coords_float[1], -1))/10]
        elif abs(coords_float[0]) > 10 and abs(coords_float[1]) < 10:
            temp = [int(round(coords_float[0], -1))/10, 0]
        elif abs(coords_float[0]) < 10 and abs(coords_float[1]) < 10:
            temp = [0, 0]
        else:
            temp = [int(round(coords_float[0], -1))/10, int(round(coords_float[1], -1))/10]
        print temp
        if temp[0] not in geonest:
            temp[0] = min([i for i in geonest], key=lambda x: abs(x-temp[0]))
        geonest = geonest.get(temp[0])
        res[0] += str(temp[0])

        if temp[1] not in geonest:
            temp[1] = min([i for i in geonest], key=lambda x: abs(x-temp[1]))
        geonest = geonest.get(temp[1])
        res[1] += str(temp[1])
        temp = [int(abs(coords_float[0])) % 10, int(abs(coords_float[1])) % 10]
        print temp
        if temp[0] not in geonest:
            temp[0] = min([i for i in geonest], key=lambda x: abs(x-temp[0]))
        geonest = geonest.get(temp[0])
        res[0] += str(temp[0]) + "."

        if temp[1] not in geonest:
            temp[1] = min([i for i in geonest], key=lambda x: abs(x-temp[1]))
        geonest = geonest.get(temp[1])
        res[1] += str(temp[1]) + "."

        coords = coords.split(",")
        for x in range(6):
            if len(coords[0][coords[0].find("."):]) - (x + 2) < 0:
                temp = 0
            else:
                temp = int(coords[0][coords[0].find(".") + x + 1])

            if temp not in geonest:
                temp = min([i for i in geonest], key=lambda x: abs(x-temp))
            geonest = geonest.get(temp)
            res[0] += str(temp)

            if len(coords[1][coords[1].find("."):]) - (x + 2) < 0:
                temp = 0
            else:
                temp = int(coords[1][coords[1].find(".") + x + 1])

            if temp not in geonest:
                temp = min([i for i in geonest], key=lambda x: abs(x-temp))
            geonest = geonest.get(temp)
            res[1] += str(temp)
        return [float(res[0]), float(res[1])]





f = open("geogrid.txt", "rb")
grid = json.load(f)
f.close()

grid2 = geogrid(grid)
print grid2.nearest("-113.497, 53.583") ## -113.49933499335006, 53.581435814358116
print grid2.nearest("-0.179, 44.0") ## 0.18180181801798745, 44.101341013410099

