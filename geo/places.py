# -*- coding: utf-8 -*-

from location import locate
import pymongo
import requests
import oauth2

client = pymongo.MongoClient()
places_db = client['test-places']
placeid_db = client['test-placeid']
geogrid = client['geogrid']

apimap = {'facebook':
              {'search':
                   {'query': 'q', 'type': 'place', 'typearg': 'type', 'coords': 'center',
                    'radius': 'distance', 'results': 'data', 'status': 'error',
                    'error': 'message', 'url': 'search'},
               'base': 'https://graph.facebook.com/', 'keyarg': "access_token",
               'key': "1665966323660099|3c2d38e96d7a0fd6dfcd0c35ea7f3303",
               'detail':
                   {'query': 'ids', 'url': '',
                    'fields': 'about,name,attire,location,website,phone,category,category_list',
                    'status': 'error', 'error': 'message', 'results': ""}
               },
          'baidu':
              {'search':
                   {'query': 'q', 'type': '', 'typearg': 'tag', 'coords': 'location',
                    'radius': 'radius', 'results': 'results', 'status': 'status',
                    'error': 'message', 'url': 'search'},
               'base': 'http://api.map.baidu.com/place/v2/', 'keyarg': "ak",
               'key': "bqhgFZml8rYqwUxv3Wk5IUrB", 'output': 'json',
               'detail':
                   {'query': 'uids', 'url': 'detail', 'results': 'result',
                    'status': 'status', 'error': 'message'}
               },
          'yandex':
              {'search':
                   {'query': 'text', 'type': 'biz', 'typearg': 'type', 'coords': 'll',
                    'radius': 'spn', 'results': 'features', 'status': 'status',
                    'error': 'message', 'url': ''},
               'base': 'https://search-maps.yandex.ru/v1/', 'keyarg': "apikey",
               'key': "9ea48cef-aa99-4d20-bf0b-1a3c38a0c190", 'lang': 'lang',
               'detail': {}
               },
          'google':
              {'search':
                   {'query': 'keyword', 'type': '', 'typearg': 'types', 'coords': 'location',
                    'radius': 'radius', 'results': 'results', 'status': 'status',
                    'error': 'message', 'url': 'nearbysearch/json'},
               'base': 'https://maps.googleapis.com/maps/api/place/', 'keyarg': "key",
               'key': "AIzaSyAgcnAoMCuhgMwXLXwRuGiEZmP0T-oWCRM", 'lang': 'language',
               'detail':
                   {'url': 'details/json', 'query': 'placeid', 'results': 'result',
                    'status': 'status', 'error': 'message'}
               },
          'yelp':
              {'search':
                   {'query': 'term', 'coords': 'll', 'radius': 'radius_filter', 'type': '',
                    'typearg': 'category_filter', 'url': 'search', 'results': 'businesses',
                    'status': 'error', 'error': 'error'},
               'base': 'https://api.yelp.com/v2/', 'lang': 'lang', 'keyarg': "a",
               'key': "a",
               'detail': {}
               }
          }

apiselect = {"Argentina": "yelp", "Australia": "yelp", "Austria": "yelp", "Belgium": "yelp", "Brazil": "yelp",
             "Canada": "yelp", "Chile": "yelp", "Czech Republic": "yelp", "Denmark": "yelp", "Finland": "yelp",
             "France": "yelp", "Germany": "yelp", "Hong Kong": "yelp", "Italy": "yelp", "Japan": "yelp",
             "Malaysia": "yelp", "Mexico": "yelp", "New Zealand": "yelp", "Norway": "yelp", "Philippines": "yelp",
             "Poland": "yelp", "Portugal": "yelp", "Republic of Ireland": "yelp", "Singapore": "yelp",
             "Spain": "yelp", "Sweden": "yelp", "Switzerland": "yelp", "Taiwan": "yelp", "The Netherlands": "yelp",
             "Turkey": "yelp", "United States": "yelp", "United Kingdom": "yelp", "Russia": "yandex",
             "India": "google", "China": "baidu"}


def get_oauth(url2, params):
    token = "B_tlIPNV3RYOu5GcnZYNq-9k8xnOxh7v"
    token_secret = "BT17FANGBppaDUuG9zzrspCzHB0"
    consumer_key = "XHQSu_eqPq7o5YNvWWozxg"
    consumer_secret = "gN2lqgKLA3psc_0UfBPplqsQN5g"
    oauth_consumer = oauth2.Consumer(key=consumer_key, secret=consumer_secret)
    oparams = {'oauth_nonce': oauth2.generate_nonce(),
               'oauth_consumer_key': consumer_key,
               'oauth_token': token,
               'oauth_timestamp': oauth2.generate_timestamp()}

    oauth_token = oauth2.Token(key=token, secret=token_secret)
    req = oauth2.Request(method='GET', parameters=params, url=url2)
    req.update(oparams)
    req.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), oauth_consumer, oauth_token)
    return req.to_url()


def places(query, coords, api="facebook", radius=5000, language="en"):
    query = query.decode("utf-8").lower().replace(u".", u"\uff0e")
    if api == "yandex":
        radius = str((radius/1000)/111.32)[:7]+","+str((radius/1000)/111.32)[:7]
        coords = [coords[1], coords[0]]
    search = places_db.posts.find_one({u"query": query, u"coords": coords, u"api": api})
    if search:
        return search[u"results"]
    method = 'search'
    smap = apimap[api][method]
    url = apimap[api]['base'] + smap['url']
    params = {
        smap['query']: str(query.encode("utf-8")),
        smap['coords']: '{0[1]},{0[0]}'.format(coords),
        smap['radius']: radius,
        smap['typearg']: smap['type'],
        apimap[api]['keyarg']: apimap[api]['key']
    }
    if 'output' in apimap[api]:
        params.update({'output': apimap[api]['output']})
    if 'lang' in apimap[api]:
        params.update({apimap[api]['lang']: language})
    if api == "yelp":
        # headers = {'User-Agent': "ONEm Communications Ltd"}
        del params[apimap[api]['keyarg']]
        url = get_oauth(url, params)
        params = {}

    r_call = requests.get(url, params)
    print r_call.url
    temp = r_call.json()
    if smap['results'] in temp:
        places_db.posts.insert_one({u"query": query, u"coords": coords, u"api": api, u"results": temp[smap['results']]})
        return temp[smap['results']]
    elif apimap[api]['status'] in temp:
        return temp[smap['status']]['error']


def placeid(query, api="facebook", language="en"):
    search = placeid_db.posts.find_one({u"query": query, u"api": api})
    if search:
        return search[u"results"]
    method = 'detail'
    smap = apimap[api][method]
    url = apimap[api]['base'] + smap['url']
    params = {
        smap['query']: query,
        apimap[api]['keyarg']: apimap[api]['key']
    }
    if 'fields' in smap:
        params.update({'fields': smap['fields']})
    if 'output' in apimap[api]:
        params.update({'output': apimap[api]['output']})
    if 'lang' in apimap[api]:
        params.update({apimap[api]['lang']: language})

    r_call = requests.get(url, params)
    print r_call.url
    temp = r_call.json()
    if smap['results'] in temp:
        placeid_db.posts.insert_one({u"query": query, u"api": api, u"results": temp[smap['results']]})
        return temp[smap['results']]
    elif api == "facebook":
        placeid_db.posts.insert_one({u"query": query, u"api": api, u"results": temp})
        return temp
    elif apimap[api]['status'] in temp:
        return temp[smap['status']]['error']


def fetch(crds):
    return geogrid.places.find_one({u"coords": {"$near": crds}})

print "test search with baidu api for food in 北京东城区东直门内大街号奇门涮肉坊(簋街总店)对面"
address = ["北京东城区东直门内大街号奇门涮肉坊(簋街总店)对面"]
query = "餐馆"
coords = locate(address)

# options integration example:
#
# if len(coords) > 1 and not location:
#   location = OptionsList(*[fetch(x)[u'city'][0]+unicode(",")+fetch(x)[u'country'][0][1] for x in coords])
#   response = "found multiple results. Please choose letter"
# elif len(coords) > 1 and location:
#   chosen_location = location.get_option_index(first_bit)
#   coords = coords[chosen_location]
#   country = fetch(coords)[u'country'][0][1]
# else:
#   coords = coords[0]
#   country = fetch(coords)[u'country'][0][1]

# then we choose the api to use based on their country:
# if fetch(coords[0])[u'country'][0][1] in apiselect:
#    api = apiselect[fetch(coords[0])[u'country'][0][1]]
#else:
#    api = "google"

# after location was shown, we show all results from places(query, coords, api=api) as another option:
# note! here each api will need a different set of parameters for the options list and ids stored
# places_call = places(query, coords, api=api)
# if places_call and not places_options:
#   places_options = OptionsList(*[x['name']+unicode(",")+x['telephone'] for x in places_call])
#   response = "send letter for more details"
# elif places_call and places_options:
#   chosen_place = places_options.get_option_index(first_bit)
#   id = places_call[chosen_location]['uid']
#   placeid_call = placeid(id, api=api)
#   ## now we can show more details about the business



if fetch(coords[0])[u'country'][0][1] in apiselect:
    api = apiselect[fetch(coords[0])[u'country'][0][1]]
else:
    api = "google"
s = places(query, coords[0], api=api)
s = placeid(s[0]['uid']+","+s[1]['uid'], api=api)
for i in s[:2]:
    print i['name'],
    if 'telephone' in i:
        print " - ", i['telephone']
    else:
        print " - "
print "="*50

print "test search with yandex api for food in ул. Блохина Санкт-Петербург Россия 197198"
address = ["ул. Блохина", "Санкт-Петербург", "Россия", "197198"]
query = "ресторан"
coords = locate(address)
if fetch(coords[0])[u'country'][0][1] in apiselect:
    api = apiselect[fetch(coords[0])[u'country'][0][1]]
else:
    api = "google"
s = places(query, coords[0], api=api, language="ru_RU")
counter = 0
for x in s:
    for j in x:
        try:
            print x[j]['name'], " - ", x[j]['CompanyMetaData']['Phones'][0]['formatted']
            counter += 1
        except:
            pass
    if counter == 2:
        break
print "="*50

print "test search with google api for food in फायर ब्रिगेड लेन बाराखंबा रो कनॉट प्लेस नई दिल्ल 110001"
address = ["फायर", "ब्रिगेड", "लेन", "बाराखंबा", "रोड", "कनॉट", "प्लेस", "नई दिल्ली", "110001"]
query = "भोजनालय"
coords = locate(address)
if fetch(coords[0])[u'country'][0][1] in apiselect:
    api = apiselect[fetch(coords[0])[u'country'][0][1]]
else:
    api = "google"
s = places(query, coords[0], api=api, language="hi")
for i in s[:2]:
    s2 = placeid(i['place_id'], api=api, language="hi")
    print s2['name'],
    if 'formatted_phone_number' in s2:
        print " - ", s2['formatted_phone_number']
    else:
        print " - "
print "="*50

print "test search with yelp api for food in newyork"
address = ["new york"]
query = "food"
coords = locate(address)
if fetch(coords[0])[u'country'][0][1] in apiselect:
    api = apiselect[fetch(coords[0])[u'country'][0][1]]
else:
    api = "google"
s = places(query, coords[0], api=api, language="en")
for i in s[:3]:
    print i['name'],
    if 'display_phone' in i:
        print " - ", i['display_phone']
    elif 'phone' in i:
        print " - ", i['phone']
    else:
        print
print "="*50

print "test search with facebook api for food in 08037 Barcelona Spain"
query = "food"
address = ["08037", "Barcelona", "Spain"]
coords = locate(address)
s = places(query, coords[0])
s = placeid(s[2]['id']+","+s[5]['id'])
for i in s:
    print s[i]['name'],
    if 'phone' in s[i]:
        print " - ", s[i]['phone']
    else:
        print " - "
