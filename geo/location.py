# -*- coding: utf-8 -*-

import ujson
from misc import params, postcode, getlastnest
import pymongo
import pycurl
import urllib
import cStringIO
import time
import re

client = pymongo.MongoClient()
geocache = client['test-geocache']
geohash = client['test-geohash']
geohashp = client['test-geohashp']
geohashc = client['test-geohashc']
geogrid = client['geogrid']


f = open("cities.txt", "rb")
citiesdb = ujson.load(f)
f.close()
# f = open("geocache.txt", "rb")
# geocache = ujson.load(f)
# f.close()
# f = open("geohash.txt", "rb")
# geohash = ujson.load(f)
# f.close()
# f = open("geogrid2.txt", "rb")
# geogrid = ujson.load(f)
# f.close()


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
    return geogrid.places.find_one({u"coords": {"$near": crds}})


def updategrid(crds, country, query):
    s = geogrid.places.find_one({u"coords": {"$near": crds}})[u'_id']
    geogrid.places.update_one(
        {u"_id": s},
        {
            "$set": {
                "country": country,
                "query": query
            }
        }
    )


def updatecache(query, results):
    entry = {u'query': query,
             u'results': results,
             u'updated': time.ctime(time.time())}
    geocache.posts.insert_one(entry)


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
                mini = (5000000, "")
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


def hashq(query, findpost, findcities):
    if findpost:
        temp6 = geohashp
        for x in findpost + findcities:
            query = re.sub(ur"{0}".format(x), u"", query, flags=re.U)
        query = re.sub(ur"  ", u" ", query, flags=re.U).strip()
        if not temp6.posts.find_one({u"query": findpost[0]}):
            temp6.posts.insert_one({u"query": findpost[0], u"nest": {}})
        temp6 = temp6.posts.find_one({u"query": findpost[0]})
        temp7 = temp6.get(u"nest")
        for x in (findpost + findcities)[1:]:
            if x not in temp7:
                temp7[x] = {}
            temp7 = temp7.get(x)
        for char in query:
            if char not in temp7:
                temp7[char] = {}
            temp7 = temp7.get(char)
        geohashp.posts.update_one({u"_id": temp6[u"_id"]},
                                  {"$set": {u"nest": temp6.get(u"nest")}})
        return [findpost, findcities, [i for i in query]]
    if findcities:
        temp6 = geohashc
        for x in findcities:
            query = re.sub(ur"{0}".format(x), u"", query, flags=re.U)
        query = re.sub(ur"  ", u" ", query, flags=re.U).strip()
        if not temp6.posts.find_one({u"query": findcities[0]}):
            temp6.posts.insert_one({u"query": findcities[0], u"nest": {}})
        temp6 = temp6.posts.find_one({u"query": findcities[0]})
        temp7 = temp6.get(u"nest")
        for x in findcities[1:]:
            if x not in temp7:
                temp7[x] = {}
            temp7 = temp7.get(x)
        for char in query:
            if char not in temp7:
                temp7[char] = {}
            temp7 = temp7.get(char)
        geohashc.posts.update_one({u"_id": temp6[u"_id"]},
                                  {"$set": {u"nest": temp6.get(u"nest")}})
        return [findcities, [i for i in query]]
    temp6 = geohash
    if not temp6.posts.find_one({u"query": query[0]}):
        temp6.posts.insert_one({u"query": query[0], u"nest": {}})
    temp6 = temp6.posts.find_one({u"query": query[0]})
    temp7 = temp6.get(u"nest")
    for char in query[1:]:
        if char not in temp7:
            temp7[char] = {}
        temp7 = temp7.get(char)
    geohash.posts.update_one({u"_id": temp6[u"_id"]},
                             {"$set": {u"nest": temp6.get(u"nest")}})
    return [[i for i in query]]


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
        temp14 = temp8.posts.find_one({u"query": query[0][0]})
        temp18 = temp14.get(u"nest")
        for x in (query[0] + query[1])[1:]:
            temp18 = temp18.get(x)
    elif len(query) == 2:
        temp8 = geohashc
        temp14 = temp8.posts.find_one({u"query": query[0][0]})
        temp18 = temp14.get(u"nest")
        for x in query[0][1:]:
            temp18 = temp18.get(x)
    else:
        temp8 = geohash
        temp14 = temp8.posts.find_one({u"query": query[0][0]})
        temp18 = temp14.get(u"nest")
        del query[0][0]
    for char in query[-1]:
        temp18 = temp18.get(char)
    if u'coords' in temp18:
        for x in coords:
            if x not in temp18[u'coords']:
                temp18[u'coords'].append(x)
    else:
        temp18[u'coords'] = coords
    temp8.posts.update_one({u"_id": temp14[u"_id"]},
                           {"$set": {u"nest": temp14[u"nest"]}})


def lookup_coords(query, findpost, findcities):
    if findpost:
        for x in findpost + findcities:
            query = re.sub(ur"{0}".format(x), u"", query, flags=re.U)
        query = re.sub(ur"  ", u" ", query, flags=re.U).strip()
        temp9 = geohashp
        if not temp9.posts.find_one({u"query": findpost[0]}):
            return False
        temp9 = temp9.posts.find_one({u"query": findpost[0]}).get(u"nest")
        for x in (findpost + findcities)[1:]:
            if x not in temp9:
                return False
            temp9 = temp9.get(x)
        for char in query:
            if char not in temp9:
                return False
            temp9 = temp9.get(char)
        if u'coords' not in temp9:
            return False
        return temp9[u'coords']
    if findcities:
        for x in findcities:
            query = re.sub(ur"{0}".format(x), u"", query, flags=re.U)
        query = re.sub(ur"  ", u" ", query, flags=re.U).strip()
        temp9 = geohashc
        if not temp9.posts.find_one({u"query": findcities[0]}):
            return False
        temp9 = temp9.posts.find_one({u"query": findcities[0]}).get(u"nest")
        for x in findcities[1:]:
            if x not in temp9:
                return False
            temp9 = temp9.get(x)

        for char in query:
            if char not in temp9:
                return False
            temp9 = temp9.get(char)
        if u'coords' not in temp9:
            return False
        return temp9[u'coords']
    temp9 = geohash
    if not temp9.posts.find_one({u"query": query[0]}):
        return False
    temp9 = temp9.posts.find_one({u"query": query[0]}).get(u"nest")
    for char in query[1:]:
        if char not in temp9:
            return False
        temp9 = temp9.get(char)
    if u'coords' not in temp9:
        return False
    return temp9[u'coords']


def locate(address):
    query = " ".join(address).lower().decode("utf-8").replace(u".", u"\uff0e")
    query, post, city = rearrange(query)
    if not lookup_coords(query, post, city):
        temp = get_geo(params(address))
        if temp['status'] == u'OK':
            updatecache(query, temp['results'])
            geohashq = hashq(query, post, city)
            coordlist = []
            for y in temp['results']:
                coords = (float(y['geometry']['location']['lng']), float(y['geometry']['location']['lat']))
                geogrident = fetch(coords)
                if geogrident[u'coords'] not in coordlist:
                    coordlist.append(geogrident[u'coords'])
                for z in y['address_components']:
                    if 'country' in z['types']:
                        country = [z['short_name'], z['long_name']]
                if u'country' in geogrident and country not in geogrident[u'country']:
                    country = geogrident[u'country'] + country
                    updategrid(coords, country, query)
                else:
                    updategrid(coords, [country], query)
            add_coords(geohashq, coordlist)
            return coordlist
        else:
            return temp
    return lookup_coords(query, post, city)


# print ["08037", "Barcelona", "Spain"], locate(["08037", "Barcelona", "Spain"])
# print ["Barcelona", "Spain", "08037"], locate(["Barcelona", "Spain", "08037"])
# print ["london"], locate(["london"])
# print ['Saint', 'Petersburg', 'Blohina', 'ulitsa'], locate(['Saint', 'Petersburg', 'Blohina', 'ulitsa'])
# print ["北京东城区东直门内大街号奇门涮肉坊(簋街总店)对面"], locate(["北京东城区东直门内大街号奇门涮肉坊(簋街总店)对面"])
# print ["ул. Блохина", "Санкт-Петербург", "Россия", "197198"],
# print locate(["ул. Блохина", "Санкт-Петербург", "Россия", "197198"])
# print ["LONDON", "liverpool", "street"], locate(["LONDON", "liverpool", "street"])
# print ['manchester'], locate(['manchester'])
# print ['manchester', "bank"], locate(['manchester', "bank"])
# print ["cismigiu", "bucuresti"], locate(["cismigiu", "bucuresti"])
# print ["liverpool"], locate(["liverpool"])
# print ["फायर", "ब्रिगेड", "लेन", "बाराखंबा", "रोड", "कनॉट", "प्लेस", "नई दिल्ली", "110001"],
# print locate(["फायर", "ब्रिगेड", "लेन", "बाराखंबा", "रोड", "कनॉट", "प्लेस", "नई दिल्ली", "110001"])

