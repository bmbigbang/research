import pymongo


client = pymongo.MongoClient()
db = client['test-database']

posts = db.posts
for k in posts.find({}):
    test = k



db = client['geogrid']
testcoord = [-0.140741, 51.503704]
s = db.places.find_one({"coords": {"$near": testcoord}})[u'_id']
print db.places.find_one({"coords": {"$near": testcoord}})


db = client['test-geocache']
testquery = u"london"
s = db.posts.find_one({"query": testquery})
print s



