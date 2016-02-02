# -*- coding: utf-8 -*-
import pymongo
import json
from pymongo import GEO2D

f = open("geogrid.txt", "rb")
geogrid = json.load(f)
f.close()

client = pymongo.MongoClient()
db = client['geogrid'].places
# create index for text search
db.create_index([("coords", GEO2D)])

for x in geogrid:
    coords = x.split(u",")
    coords = [coords[0].lstrip(u"("), coords[1].rstrip(u")")]
    coords = [round(float(coords[0]), 6), round(float(coords[1]), 6)]
    entry = {u"city": [], u"country": [], u'query': [], u"coords": coords, u"postcode": []}
    db.insert_one(entry)
