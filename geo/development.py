# -*- coding: utf-8 -*-

import ujson
from misc import repeat, getlastnest, postcode
from math import sqrt
import operator
import re
import pymongo

# f = open("geocache.txt", "rb")
# geocache = ujson.load(f)
# f.close()

client = pymongo.MongoClient()

f = open("cities.txt", "rb")
citiesdb = ujson.load(f)
f.close()

geohash = {}
geohashp = {}
geohashc = {}


def lookup_closest(query):
    if len(query) == 3:
        temp10 = geohashp
        for x in query[0] + query[1]:
            temp10 = temp10.get(x)
    elif len(query) == 2:
        temp10 = geohashc
        for x in query[0]:
            temp10 = temp10.get(x)
    else:
        temp10 = geohash
    counter = 0
    for char in query[-1]:
        if not temp10:
            return []
        if char in temp10:
            temp10 = temp10.get(char)
        elif len(temp10) == 1 and 'coords' not in temp10:
            for x in temp10:
                temp10 = temp10.get(x)
            counter += 1
        elif len(temp10) == 2 and 'coords' in temp10:
            for x in temp10:
                temp10 = temp10.get(x)
            counter += 1
        elif temp10:
            counter += 1
            mini = (50000, "")
            for x in temp10:
                if len(x) > 1:
                    continue
                dist = abs((ord(x) - ord(char)))
                if mini[0] > dist:
                    mini = (dist, x)
            if mini[1]:
                temp10 = temp10.get(mini[1])
        if counter >= 3:
            return []
    if not temp10:
        return []
    if 'coords' in temp10:
        return temp10['coords']
    args = []
    for y in temp10:
        if 'coords' in temp10[y]:
            return temp10[y]['coords']
        args.append(y)
    return repeat(temp10, args)


def fetch(crds):
    db = client['test-geogrid']
    return db.places.find_one({"coords": {"$near": crds}})


def hashq(query, findpost, findcities):
    if findpost:
        temp6 = geohashp
        for x in findpost + findcities:
            query = re.sub(ur"{0}".format(x), u"", query, flags=re.U)
        query = re.sub(ur"  ", u" ", query, flags=re.U).strip()
        for x in findpost + findcities:
            if x not in temp6:
                temp6[x] = {}
            temp6 = temp6.get(x)
        for char in query:
            if char not in temp6:
                temp6[char] = {}
            temp6 = temp6.get(char)
        return [findpost, findcities, [i for i in query]]
    if findcities:
        temp6 = geohashc
        for x in findcities:
            query = re.sub(ur"{0}".format(x), u"", query, flags=re.U)
        query = re.sub(ur"  ", u" ", query, flags=re.U).strip()
        for x in findcities:
            if x not in temp6:
                temp6[x] = {}
            temp6 = temp6.get(x)
        for char in query:
            if char not in temp6:
                temp6[char] = {}
            temp6 = temp6.get(char)
        return [findcities, [i for i in query]]
    temp6 = geohash
    for char in query:
        if char not in temp6:
            temp6[char] = {}
        temp6 = temp6.get(char)
    return [[i for i in query]]


def cities(query):
    parts = re.split(ur"\s", query, flags=re.U)
    foundcities = []
    for x in parts:
        letters = ""
        counter = 0
        temp10 = citiesdb
        for char in x:
            if char in temp10:
                temp10 = temp10.get(char)
                letters += char
            elif len(temp10) == 1 and unicode("*|") not in temp10:
                for y in temp10:
                    temp10 = temp10.get(y)
                    letters += y
                counter += 1
            elif len(temp10) == 2 and unicode("*|") in temp10:
                for y in temp10:
                    if y != unicode("*|"):
                        temp10 = temp10.get(y)
                        letters += y
                counter += 1
            elif temp10:
                mini = (50000, "")
                for y in temp10:
                    if y == unicode("*|"):
                        continue
                    dist = abs((ord(y) - ord(char)))
                    if mini[0] > dist:
                        mini = (dist, y)
                counter += 1
                if mini[1]:
                    temp10 = temp10.get(mini[1])
                    letters += mini[1]
            if counter >= 3 or not temp10:
                break
        if unicode("*|") not in temp10:
            if getlastnest(temp10):
                letters += getlastnest(temp10)
            else:
                continue
        if abs(len(letters)-len(x)) >= 3:
            continue
        if counter <= 3:
            foundcities.append((letters, x, counter))
    return foundcities


def rearrange(query):
    query = query.lower()
    findpost = postcode(query)
    if findpost:
        for x in findpost:
            query = re.sub(ur"{0}".format(x), u"", query, flags=re.U).strip()
            query = re.sub(ur"  ", u" ", query, flags=re.U)
    findcities = [i[0] for i in cities(query) if i[2] <= 2]
    if findcities:
        for x in findcities:
            query = re.sub(ur"{0}".format(x), u"", query, flags=re.U).strip()
            query = re.sub(ur"  ", u" ", query, flags=re.U)
        if findpost:
            query = " ".join(findpost) + " " + " ".join(findcities) + " " + query
        else:
            query = " ".join(findcities) + " " + query
    elif findpost:
        query = " ".join(findpost) + " " + query
    return query, findpost, findcities


def add_coords(query, coords):
    if len(query) == 3:
        temp8 = geohashp
        for x in query[0] + query[1]:
            temp8 = temp8.get(x)
    elif len(query) == 2:
        temp8 = geohashc
        for x in query[0]:
            temp8 = temp8.get(x)
    else:
        temp8 = geohash
    for letter in query[-1]:
        temp8 = temp8.get(letter)
    if 'coords' in temp8:
        for x in coords:
            if x not in temp8['coords']:
                temp8['coords'].append(x)
    else:
        temp8['coords'] = coords


def lookup_coords(query):
    if len(query) == 3:
        temp9 = geohashp
        for x in query[0] + query[1]:
            temp9 = temp9.get(x)
        for char in query[2]:
            temp9 = temp9.get(char)
        return temp9['coords']
    elif len(query) == 2:
        temp9 = geohashc
        for x in query[0]:
            temp9 = temp9.get(x)
        for char in query[1]:
            temp9 = temp9.get(char)
        return temp9['coords']
    temp9 = geohash
    for letter in query[0]:
        temp9 = temp9.get(letter)
    return temp9['coords']


# for x in geocache:
#     query, post, city = rearrange(x)
#     print x, " - ", query
#     geohashq = hashq(query, post, city)
#     coordlist = []
#     for y in geocache[x][0]:
#         coords = (float(y['geometry']['location']['lng']), float(y['geometry']['location']['lat']))
#         temp3 = fetch(coords)['coords']
#         if temp3 not in coordlist:
#             coordlist.append(temp3)
#     add_coords(geohashq, coordlist)
#     print x, lookup_coords(geohashq)
#     print coordlist

# postcode test
# test = """1341135, kt12 5le, 311241, UK251, 13515-124,
# sa2134, b2b c2c, gf5-1353, 123 55, 12m n12, sd-1353, (1111), (135-135), 245-cd,
#  1341135 kt12 5le 311241 wfq.31q 245-cd sd-1353 test test 123"""
# print postcode(test)
# test2 = """௧௨௩௪௫௬௭"""
# print postcode(test2.decode("utf-8"))
# print cities('liverpo')
# print cities('liverpoo')
# print lookup_closest([['london', 'liver'], []])



