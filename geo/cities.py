# -*- coding: utf-8 -*-
import csv
import copy
import ujson

with open("GeoLite2-City-Locations-en.csv", "rb") as f:
    s = csv.reader(f, dialect="excel")
    grid = []
    for i in s:
        if i[-3] and "_" not in i[-3]:
            grid.append(copy.deepcopy(i[-3].decode("utf-8")))

f.close()
grid2 = {}
grid.append("saint")
for i in grid:
    test = grid2
    for j in i:
        j = j.lower()
        if j not in test:
            test[j] = {}

        test = test.get(j)
    test[unicode("*|")] = 0

# counter = 0; args = []
# for i in grid2:
#     counter += 1
#     args.append(i)
f = open("cities.txt", "wb")
ujson.dump(grid2, f, ensure_ascii=False)
f.close()
for i in grid2['s']['a']['i']['n']['t']['s']:
    print i
# def repeat(nest, args3):
#     args2 = []
#     c = 0
#     for z in args3:
#         temp2 = nest.get(z)
#         if temp2:
#             for y in temp2:
#                 args2.append(y)
#                 c += 1
#             c += repeat(temp2, args2)
#
#     return c
#
# test2 = {"b": {"BB": {}, "BC": {}, "CC": {}}}
# test = {"a":{"A":{},"B":{}}}
# test = {"a":{"A":{"c":{},"d":{}},"B":test2},"b":test2}
# print repeat(test, ['a'])
