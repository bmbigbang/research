# -*- coding: utf-8 -*-

# import csv
# import copy
import ujson
import re
import pymongo
import bson
import urllib
import pycurl
import cStringIO
import time
import dateparser
import datetime

# with open("airlines.dat", "rb") as f:
#     s = csv.reader(f)
#     data = []
#     for i in s:
#         data.append(copy.deepcopy(i))
# f.close()
# airlines = {}
# airlinesiata = {}
# for x in data:
#     if x[3]:
#         temp = airlinesiata
#         for y in x[3].decode("utf-8"):
#             if y not in temp:
#                 temp[y] = {}
#             temp = temp.get(y)
#         if x[4]:
#             if unicode("*|") in temp:
#                 if len(x[1].split()) < 2:
#                     temp[unicode("*|")] = x[4].decode("utf-8")
#             else:
#                 temp[unicode("*|")] = x[4].decode("utf-8")
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
            if mini[1]:
                temp = temp.get(mini[1])
                query = re.sub(ur"{0}".format(x), u'{0}'.format(mini[1]), query[:3], flags=re.U|re.I) + query[3:]
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
print airlines['B']['A']
print "BAQ 5", airline("BAQ 5")

client = pymongo.MongoClient()
airports_db = client['test-airports'].airports
flights_db = client['test-flights'].flights


def airport(query, detail=False):
    if detail:
        return airports_db.find_one({u"iata": query})
    query = unicode(query.lower())
    query = re.sub(u"intl", u'international', query, flags=re.U|re.I)
    res = []
    # for i in airports_db.find({"$text": {'$search': query}}, {}):
    #     res.append(airports_db.find_one(i))
    # if res:
    #     return res
    pattern = re.compile(ur'{0}'.format(query), flags=re.U|re.I)
    regex = bson.regex.Regex.from_native(pattern)
    for i in airports_db.find({u"name": {"$regex": regex}}, {}):
        res.append(airports_db.find_one(i))
    if not res:
        return []
    ## here options will be integrated to decide which airport to query for
    return res


def airportFIDS(airp, direction):
    if not airp:
        return "Airport not found"
    direction = unicode(direction)
    if u'{0}_updated'.format(direction) in airp[0]:
        if float(airp[0][u'{0}_updated'.format(direction)]) + (3600*12) > time.time():
            return airp[0][u"{0}".format(direction)]
    params = {
        'appId': "9cde3a13",
        'appKey': "d252594ac2904e9d65dc2beb7d192321",
        'codeType': "IATA",
        'requestedFields': 'flightId,flight,airportCode,currentTime,scheduledTime,currentDate,terminal,gate,remarks',
        'sortFields': 'scheduledTime',
        'lateMinutes': '15'
    }
    base = "https://api.flightstats.com/flex/fids/rest/v1/json/"
    airporturl = "{0}/{1}?".format(str(airp[0][u'iata']), str(direction))
    url = base + airporturl
    print url + urllib.urlencode(params)
    c.reset()
    c.setopt(c.URL, url + urllib.urlencode(params))
    c.setopt(c.WRITEDATA, bufr)
    c.perform()
    temp = ujson.loads(bufr.getvalue())
    airports_db.update_one({u"_id": airp[0][u"_id"]},
                           {"$set": {u"{0}".format(direction): temp,
                                     u'{0}_updated'.format(direction): time.time()}})
    bufr.truncate(0)
    return temp


def flight(flightid, date=u""):
    if not airline(flightid):
        return "Error with flight ID - airline check"
    flightid = flightid.split()
    year = time.strftime("%Y")
    month = time.strftime("%m")
    day = time.strftime("%d")
    if date:
        now = datetime.datetime(int(year), int(month), int(day)).toordinal()
        date = dateparser.parse(date)
        if date.toordinal() - (3600*24*3) > now:
            return "Error with date, can only look for flights 3 days in advance"
        year = "{0}".format(date.year)
        month = "{:02d}".format(date.month)
        day = "{:02d}".format(date.day)
    args = "{0}/{1}/dep/{2}/{3}/{4}".format(flightid[0], flightid[1], year, month, day)
    search = flights_db.find_one({u"flightargs": args})
    if search:
        if u'updated' in search:
            if search[u'updated'] == time.strftime("%d"):
                return search[u'results']
    base = "https://api.flightstats.com/flex/flightstatus/rest/v2/json/flight/status/"
    params = "?appId=9cde3a13&appKey=d252594ac2904e9d65dc2beb7d192321&utc=false"
    url = base + args + params
    print url
    c.reset()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, bufr)
    c.perform()
    temp = ujson.loads(bufr.getvalue())
    bufr.truncate(0)
    if not temp['flightStatuses']:
        return "Error with flight status query - empty response"
    if search:
        flights_db.update_one({u"_id": search[u"_id"]},
                              {"$set": {u"results": temp,
                                        u'updated': time.strftime("%d")}})
    else:
        flights_db.insert_one({u"results": temp, u'updated': time.strftime("%d"),
                               u"flightargs": args})
    return temp

bufr = cStringIO.StringIO()
c = pycurl.Curl()

testquery = airportFIDS(airport("belfast intl"), "departures")[u'fidsData']
for x in testquery[:5]:
    print "Flight ID:", x[u'flight'] + ", set for departure at:", x[u'scheduledTime'], ", is", x[u'remarks']
    testquery2 = airport(x[u'airportCode'], detail=True)
    print "Destination:", testquery2[u'name'].title() + ",", testquery2[u'city'].title() + ",", \
        testquery2[u'country'].title(), "- Airline:", airline(x[u'flight'])[1]
    print "-" * 50
testquery = airportFIDS(airport("fast"), "arrivals")[u'fidsData']
for x in testquery[:5]:
    print "Flight ID:", x[u'flight'] + ", set for arrival at:", x[u'scheduledTime'], ", is", x[u'remarks']
    testquery2 = airport(x[u'airportCode'], detail=True)
    print "Destination:", testquery2[u'name'].title() + ",", testquery2[u'city'].title() + ",", \
        testquery2[u'country'].title(), "- Airline:", airline(x[u'flight'])[1]
    print "-" * 50

print "Flight check test with U2 6748 (this is date sensitive)"
tq = flight("U2 6704")[u'flightStatuses'][0]
print "Flight ID:", tq["carrierFsCode"], tq["flightNumber"], "- Flight Duration:",\
    tq["flightDurations"]["scheduledBlockMinutes"], "Minutes"
tq2 = airport(tq["departureAirportFsCode"], detail=True)
print "From", tq2[u'name'].title() + ",", tq2[u'city'].title() + ",", tq2[u'country'].title()
tq2 = airport(tq["arrivalAirportFsCode"], detail=True)
print "To", tq2[u'name'].title() + ",", tq2[u'city'].title() + ",", tq2[u'country'].title()
print "Departure Date:", tq['departureDate']['dateLocal'], "Local,", tq['departureDate']['dateUtc'], "UTC"
print "Arrival Date:", tq['arrivalDate']['dateLocal'], "Local,", tq['arrivalDate']['dateUtc'], "UTC"

print "Flight check test with LH 925 on 3 feb 16"
tq = flight("LH 925", date=u'3 feb 16')[u'flightStatuses'][0]
print "Flight ID:", tq["carrierFsCode"], tq["flightNumber"], "- Flight Duration:",\
    tq["flightDurations"]["scheduledBlockMinutes"], "Minutes"
tq2 = airport(tq["departureAirportFsCode"], detail=True)
print "From", tq2[u'name'].title() + ",", tq2[u'city'].title() + ",", tq2[u'country'].title()
tq2 = airport(tq["arrivalAirportFsCode"], detail=True)
print "To", tq2[u'name'].title() + ",", tq2[u'city'].title() + ",", tq2[u'country'].title()
print "Departure Date:", tq['departureDate']['dateLocal'], "Local,", tq['departureDate']['dateUtc'], "UTC"
print "Arrival Date:", tq['arrivalDate']['dateLocal'], "Local,", tq['arrivalDate']['dateUtc'], "UTC"

c.close()
bufr.close()

