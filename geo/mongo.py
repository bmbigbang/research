import pymongo
from misc import repeat


client = pymongo.MongoClient()
db = client['test-database']

posts = db.posts
for k in posts.find({}):
    test = k


def lookup_closest(query):
    temp10 = test
    counter = 0
    for char in query.lower():
        if char in temp10:
            temp10 = temp10.get(char)
        elif len(temp10) == 1 and 'coords' not in temp10:
            for x in temp10:
                temp10 = temp10.get(x)
            counter += 1
        else:
            min = (0, "")
            for x in temp10:
                if len(x) != 1:
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

print lookup_closest('Londn')

db = client['test-geogrid']
testcoord = [-0.140741, 51.503704]
s = db.places.find_one({"coords": {"$near": testcoord}})[u'_id']
db.places.update_one(
    {u"_id": s},
    {
        "$set": {
            "country": [],
            "query": []
        }
    }
)
print db.places.find_one({"coords": {"$near": testcoord}})


db = client['test-geocache']
testquery = u"london"
s = db.posts.find_one({"query": testquery})
print s



