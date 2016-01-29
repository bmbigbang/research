# -*- coding: utf-8 -*-

import csv
import copy
import ujson
import re
import pymongo
import bson


# with open("airlines.dat", "rb") as f:
#     s = csv.reader(f)
#     routes = []
#     for i in s:
#         routes.append(copy.deepcopy(i))
# f.close()
# airlines = {}
# airlinesiata = {}
# for x in routes:
#     if x[3]:
#         temp = airlinesiata
#         for y in x[3].decode("utf-8"):
#             if y not in temp:
#                 temp[y] = {}
#             temp = temp.get(y)
#         temp[unicode("*|")] = x[4].decode("utf-8")
#     temp = airlines
#     for y in x[4].decode("utf-8"):
#         if y not in temp:
#             temp[y] = {}
#         temp = temp.get(y)
#     temp[unicode("*|")] = [x[1].decode("utf-8"), x[-2].decode("utf-8")]
#
# f = open("airlines.txt", "wb")
# ujson.dump(airlines, f, ensure_ascii=False)
# f.close()
# f = open("airlinesiata.txt", "wb")
# ujson.dump(airlinesiata, f, ensure_ascii=False)
# f.close()

f = open("airlines.txt", "rb")
airlines = ujson.load(f)
f.close()
f = open("airlinesiata.txt", "rb")
airlinesiata = ujson.load(f)
f.close()


def airline(query):
    query = query.decode("utf-8").upper()
    temp = airlinesiata
    pattern = re.compile(ur"[a-z]{3}", flags=re.U|re.I)
    if not re.match(pattern, query):
        for x in query[:2]:
            if x in temp:
                temp = temp.get(x)
        if unicode("*|") in temp:
            query = query.replace(query[:2], temp[unicode("*|")])
    pattern = re.compile(ur"[\- ]?\d{1,4}[a-z]?", flags=re.U|re.I)
    if not re.search(pattern, query):
        return []
    temp = airlines
    counter = 0
    for x in [i for i in query[:3]]:
        if x in temp:
            temp = temp.get(x)
        elif len(temp) > 1:
            counter += 1
            mini = (5000000, "")
            for y in temp:
                if len(y) > 1:
                    continue
                dist = abs((ord(y) - ord(x)))
                if mini[0] > dist:
                    mini = (dist, y)
            temp = temp.get(mini[1])
        elif unicode("*|") not in temp:
            counter += 1
            for z in temp:
                temp.get(z)
        if counter > 1:
            return []
    if not temp:
        return []
    if unicode("*|") in temp:
        return ["".join([i for i in query[:3]])] + temp[unicode("*|")]
    return []

print airlines['B']['A']
print "BA324", airline("BA324")
print "BA-54", airline("BA-54")
print "BA 5", airline("BA 5")
print "Qr 5S", airline("QR 5S")
print "QRT 5S", airline("QRT 5S")
print "BS 534S", airline("BS 534S")
print "IATA code example:"
print "Z3", airlinesiata['Z']['3']
print "Z3 534S", airline("Z3 534S")
print "correction example:"
print "BAQ 5", airline("BAQ 5")

client = pymongo.MongoClient()
airports_db = client['test-airports'].airports


def airport(query):
    query = query.lower()
    appid = "9cde3a13"
    appkey = "d252594ac2904e9d65dc2beb7d192321"
    res = []
    for i in airports_db.find({"$text": {'$search': query}}, {}):
        res.append(airports_db.find_one(i))
    if res:
        return res
    pattern = re.compile(ur'{0}'.format(query), flags=re.U|re.I)
    regex = bson.regex.Regex.from_native(pattern)
    for i in airports_db.find({"name": {"$regex": regex}}, {}):
        res.append(airports_db.find_one(i))
    return res

print [i['name'] for i in airport("Belfast")]
print [i['name'] for i in airport("belf")]
