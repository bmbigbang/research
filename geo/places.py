# -*- coding: utf-8 -*-

import urllib
import pycurl
import ujson
import cStringIO
from location import locate


apimap = {'facebook':
              {'search':
                   {'query': 'q', 'type': 'place', 'typearg': 'type', 'coords': 'center',
                    'radius': 'distance', 'results': 'data', 'status': 'error',
                    'error': 'message', 'url': 'search?'},
               'base': 'https://graph.facebook.com/', 'keyarg': "access_token",
               'key': "1665966323660099|3c2d38e96d7a0fd6dfcd0c35ea7f3303",
               'detail': {'query': 'ids', 'url': '?',
                          'fields': 'about,name,attire,location,website,phone,category,category_list',
                          'status': 'error', 'error': 'message', 'results': ""}
               },
          'baidu':
              {'search':
                   {'query': 'q', 'type': '', 'typearg': 'tag', 'coords': 'location',
                    'radius': 'radius', 'results': 'results', 'status': 'status',
                    'error': 'message', 'url': 'search?'},
               'base': 'http://api.map.baidu.com/place/v2/', 'keyarg': "ak",
               'key': "bqhgFZml8rYqwUxv3Wk5IUrB", 'output': 'json',
               'detail': {'query': 'uids', 'url': 'detail?', 'results': 'result',
                          'status': 'status', 'error': 'message'}
               },
          'yandex':
              {'search':
                   {'query': 'text', 'type': 'biz', 'typearg': 'type', 'coords': 'll',
                    'radius': 'spn', 'results': 'features', 'status': 'status',
                    'error': 'message', 'url': '?'},
               'base': 'https://search-maps.yandex.ru/v1/', 'keyarg': "apikey",
               'key': "9ea48cef-aa99-4d20-bf0b-1a3c38a0c190", 'lang': 'lang',
               'detail': {}
               },
          'google':
              {'search':
                   {'query': 'keyword', 'type': '', 'typearg': 'types', 'coords': 'location',
                    'radius': 'radius', 'results': 'results', 'status': 'status',
                    'error': 'message', 'url': 'radarsearch/json?'},
               'base': 'https://maps.googleapis.com/maps/api/place/', 'keyarg': "key",
               'key': "AIzaSyAgcnAoMCuhgMwXLXwRuGiEZmP0T-oWCRM", 'lang': 'language',
               'detail': {'url': 'details/json?', 'query': 'placeid', 'results': 'result',
                          'status': 'status', 'error': 'message'}
               }
          }


def places(query, coords, api="facebook", radius=5000, language="en"):
    method = 'search'
    smap = apimap[api][method]
    url = apimap[api]['base'] + smap['url']
    if api == "yandex":
        radius = str((radius/1000)/111.32)[:7]+","+str((radius/1000)/111.32)[:7]
        coords = [coords[1], coords[0]]
    params = {
        smap['query']: query,
        smap['coords']: '{0},{1}'.format(coords[1], coords[0]),
        smap['radius']: radius,
        smap['typearg']: smap['type'],
        apimap[api]['keyarg']: apimap[api]['key']
    }
    if 'output' in apimap[api]:
        params.update({'output': apimap[api]['output']})
    if 'lang' in apimap[api]:
        params.update({apimap[api]['lang']: language})
    print url + urllib.urlencode(params)
    c.reset()
    c.setopt(c.URL, url + urllib.urlencode(params))
    c.setopt(c.WRITEDATA, bufr)
    c.perform()
    temp = ujson.loads(bufr.getvalue())
    bufr.truncate(0)
    if smap['results'] in temp:
        return temp[smap['results']]
    elif apimap[api]['status'] in temp:
        return temp[smap['status']]['error']


def placeid(query, api="facebook", language="en"):
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
    print url + urllib.urlencode(params)
    c.reset()
    c.setopt(c.URL, url + urllib.urlencode(params))
    c.setopt(c.WRITEDATA, bufr)
    c.perform()
    temp = ujson.loads(bufr.getvalue())
    bufr.truncate(0)
    if smap['results'] in temp:
        return temp[smap['results']]
    elif api == "facebook":
        return temp
    elif apimap[api]['status'] in temp:
        return temp[smap['status']]['error']


bufr = cStringIO.StringIO()
c = pycurl.Curl()
# query = "food"
# address = ["08037", "Barcelona", "Spain"]
# coords, country = locate(address)
# if u"ES" in [j for i in country for j in i]:
#     s = places(query, coords[0])
#     s = placeid(s[0]['id']+","+s[1]['id'])
#     for i in s:
#         print s[i]['name'],
#         if 'phone' in s[i]:
#             print " - ", s[i]['phone']
#         else:
#             print "/n"
#     c.close()
#     c = pycurl.Curl()
#
# address = ["北京东城区东直门内大街号奇门涮肉坊(簋街总店)对面"]
# query = "餐馆"
# coords, country = locate(address)
# if u"China" in [j for i in country for j in i]:
#     s = places(query, coords[0], api="baidu")
#     s = placeid(s[0]['uid']+","+s[1]['uid'], api="baidu")
#     for i in s[:2]:
#         print i['name'],
#         if 'telephone' in i:
#             print " - ", i['telephone']
#         else:
#             print "/n"
#     c.close()
#     c = pycurl.Curl()
#
# address = ["ул. Блохина", "Санкт-Петербург", "Россия", "197198"]
# query = "ресторан"
# coords, country = locate(address)
# if u"Russia" in [j for i in country for j in i]:
#     s = places(query, coords[0], api="yandex", language="ru_RU")
#     counter = 0
#     for x in s:
#         for j in x:
#             try:
#                 print x[j]['name'], " - ", x[j]['CompanyMetaData']['Phones'][0]['formatted']
#                 counter += 1
#             except:
#                 pass
#         if counter == 2:
#             break
#     c.close()
#
# address = ["फायर", "ब्रिगेड", "लेन", "बाराखंबा", "रोड", "कनॉट", "प्लेस", "नई दिल्ली", "110001"]
# query = "भोजनालय"
# coords, country = locate(address)
# if u"India" in [j for i in country for j in i]:
#     s = places(query, coords[0], api="google", language="hi")
#     for i in s[:2]:
#         s2 = placeid(i['place_id'], api="google", language="hi")
#         print s2['name'],
#         if 'formatted_phone_number' in s2:
#             print " - ", s2['formatted_phone_number']
#         else:
#             print "/n"

c.close()
bufr.close()

