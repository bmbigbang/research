# -*- coding: utf-8 -*-
import pymongo
import csv
import copy
import re
import bson

client = pymongo.MongoClient()
airports_db = client['test-airports'].airports

# with open("airports.dat", "rb") as f:
#     s = csv.reader(f)
#     temp = []
#     for i in s:
#         temp.append(copy.deepcopy(i))
# f.close()
#
# # create index for text search
# airports_db.create_index([("name", "text")])
#
# for x in temp:
#     # Timezone	Hours offset from UTC. Fractional hours are expressed as decimals, eg. India is 5.5.
#     # DST (Daylight savings time): One of E (Europe), A (US/Canada), S (South America),
#     #  O (Australia), Z (New Zealand), N (None) or U (Unknown).
#     # zz database time zone	Timezone in "tz" (Olson) format, eg. "America/Los_Angeles".
#     # tz data is ISO 8859-1 (Latin-1) encoded, with no special characters.
#     x[1] = re.sub(u"intl", u'international', x[1], flags=re.U|re.I)
#     entry = {
#         "name": x[1].decode("utf-8").lower(), "city": x[2].decode("utf-8").lower(),
#         "country": x[3].decode("utf-8").lower(), "iata": x[4].decode("utf-8") if x[4] else u"",
#         "icao": x[5].decode("utf-8"), "coords": [float(x[7]), float(x[6])],
#         "altitude": x[8], "timezone": x[9], "DST": x[10], "tz": x[11]
#     }
#     airports_db.insert_one(entry)

# example search methods:
query = "belfast"
for i in airports_db.find({"$text": {'$search': query}}, {}):
    print airports_db.find_one(i)

print "-"*50

pattern = re.compile(ur'belfast intl', flags=re.U|re.I)
regex = bson.regex.Regex.from_native(pattern)
for i in airports_db.find({"name": {"$regex": regex}}, {}):
    print airports_db.find_one(i)
