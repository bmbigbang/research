# -*- coding: utf-8 -*-

import ujson
from misc import pop_dec
from math import sqrt
import operator
import time

f = open("geocache.txt", "rb")
geocache = ujson.load(f)
f.close()

f = open("geogrid2.txt", "rb")
geogrid = ujson.load(f)
f.close()

geohash = {}


def closest(vec, nest):
    s = {}
    for x in nest:
        p = x.lstrip("(").rstrip(")").split(",")
        s[x] = abs(sqrt((int(p[0])**2) + int(p[1])**2) - vec)
    s = sorted(s.items(), key=operator.itemgetter(1))
    return s[0][0]


def lookup_closest(query):
    temp10 = geohash
    counter = 0
    for char in query:
        if char in temp10:
            temp10 = temp10.get(char)
        elif len(temp10) == 1 and 'coords' not in temp10:
            for x in temp10:
                temp10 = temp10.get(x)
            counter += 1
        else:
            min = (0, "")
            for x in temp10:
                if x == 'coords':
                    continue
                dist = abs((ord(x) - ord(char)))
                if min[0] < dist:
                    min = (dist, x)
            counter += 1
            temp10 = temp10.get(min[1])
        if counter >= 3:
            return []

    if 'coords' in temp10:
        return temp10['coords']
    args = []
    for y in temp10:
        if 'coords' in temp10[y]:
            return temp10[y]['coords']
        args.append(y)
    return repeat(temp10, args)


def repeat(nest, args):
    temp1 = nest
    coords = []
    args2 = []
    for z in args:
        temp1 = temp1.get(z)
        if temp1:
            for y in temp1:
                if 'coords' in temp1[y]:
                    coords += temp1[y]['coords']
                else:
                    args2.append(y)
            coords += repeat(temp1, args2)
    return coords


def fetch(crds):
    p = (int(crds[0]) / 10, int(crds[1]) / 10)
    if str(p) not in geogrid:
        vec = sqrt(p[0]**2 + p[1]**2)
        temp4 = geogrid[closest(vec, geogrid)]
    else:
        temp4 = geogrid[str(p)]
    p = (int(crds[0]) % 10, int(crds[1]) % 10)
    if str(p) not in temp4:
        vec = sqrt(p[0]**2 + p[1]**2)
        temp4 = temp4[closest(vec, temp4)]
    else:
        temp4 = temp4[str(p)]
    temp5 = pop_dec(crds)
    for z in temp5:
        if str(z) in temp4:
            temp4 = temp4.get(str(z))
        elif u'query' in temp4:
            return temp4
        else:
            vec = sqrt((z[0]**2)+(z[1]**2))
            temp4 = temp4.get(closest(vec, temp4))
    return temp4


def hashq(query):
    temp6 = geohash
    for char in query:
        if char in temp6:
            temp6 = temp6.get(char)
        else:
            temp6[char] = {}
            temp6 = temp6.get(char)


def add_coords(query, coords):
    temp8 = geohash
    for letter in query:
        temp8 = temp8.get(letter)
    if 'coords' in temp8:
        for x in coords:
            if x not in temp8['coords']:
                temp8['coords'].append(x)
    else:
        temp8['coords'] = coords
    return


def lookup_coords(query):
    temp9 = geohash
    for letter in query:
        temp9 = temp9.get(letter)
    return temp9['coords']

geocache['london2'] = [[{'geometry': {'location': {'lng': '100.0', 'lat': '20.0'}}}], 0]
geocache['london2 liverpool'] = [[{'geometry': {'location': {'lng': '100.0', 'lat': '20.0'}}}], 0]

for x in geocache:
    hashq(x.lower())
    coordlist = []
    for y in geocache[x][0]:
        coords = (float(y['geometry']['location']['lng']), float(y['geometry']['location']['lat']))
        temp3 = fetch(coords)['coords']
        if temp3 not in coordlist:
            coordlist.append(temp3)
    add_coords(x.lower(), coordlist)

for x in geocache:
    print x, lookup_coords(x.lower())
    coordlist = []
    for y in geocache[x][0]:
        coords2 = (float(y['geometry']['location']['lng']), float(y['geometry']['location']['lat']))
        temp3 = fetch(coords2)['coords']
        coordlist.append(["fetch(coords)", temp3, "coords", coords2])

# print geohash['l']['o']['n']['d']['o']['n'][' ']
# print geohash['l']['o']['n']['d']['o']['n']['2']

print lookup_closest('saint')