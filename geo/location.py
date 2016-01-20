# -*- coding: utf-8 -*-

import ujson
from misc import pop_dec, params, closest, repeat
from math import sqrt
import pycurl
import urllib
import cStringIO
import time

f = open("geocache.txt", "rb")
geocache = ujson.load(f)
f.close()
f = open("geohash.txt", "rb")
geohash = ujson.load(f)
f.close()
f = open("geogrid2.txt", "rb")
geogrid = ujson.load(f)
f.close()


def get_geo(prms):
    bufr = cStringIO.StringIO()
    base = "https://maps.googleapis.com/maps/api/geocode/json?"
    print base + urllib.urlencode(prms)
    c = pycurl.Curl()
    c.setopt(c.URL, base + urllib.urlencode(prms))
    c.setopt(c.WRITEDATA, bufr)
    c.perform()
    c.close()
    t = ujson.loads(bufr.getvalue())
    bufr.close()
    return t


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
    for char in query.lower():
        if char in temp6:
            temp6 = temp6.get(char)
        else:
            temp6[char] = {}
            temp6 = temp6.get(char)


def add_coords(query, coords):
    temp8 = geohash
    for letter in query.lower():
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
    for letter in query.lower():
        temp9 = temp9.get(letter)
    return temp9['coords']


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


def locate(address):
    query = " ".join(address).lower().decode("utf-8")
    if not lookup_coords(query):
        temp = get_geo(params(address))
        if temp['status'] == u'OK':
            geocache.update({query: (temp['results'], time.ctime(time.time()))})
            f = open("geocache.txt", "wb")
            ujson.dump(geocache, f)
            f.close()
            hashq(query)
            coordlist = []
            for y in temp['results']:
                coords = (float(y['geometry']['location']['lng']), float(y['geometry']['location']['lat']))
                temp3 = fetch(coords)
                coordlist.append(temp3['coords'])
                for z in y['address_components']:
                    if 'country' in z['types']:
                        if [z['short_name'], z['long_name']] not in temp3['country']:
                            temp3['country'].append([z['short_name'], z['long_name']])
            add_coords(query, coordlist)
            f = open("geogrid2.txt", "wb")
            ujson.dump(geogrid, f)
            f.close()
            f = open("geohash.txt", "wb")
            ujson.dump(geohash, f)
            f.close()
        else:
            return temp
    return lookup_coords(query), fetch(lookup_coords(query)[0])['country']

print locate(["08037", "Barcelona", "Spain"])
print locate(["london"])
print locate(['Saint Petersburg', 'Blohina ulitsa'])
print locate(["北京东城区东直门内大街号奇门涮肉坊(簋街总店)对面"])
print locate(["ул. Блохина", "Санкт-Петербург", "Россия", "197198"])
print locate(["LONDON", "liverpool", "street"])
print locate(['manchester'])
print locate(['manchester', "bank"])
print locate(["cismigiu","bucuresti"])

print lookup_closest('saint petersburg')
