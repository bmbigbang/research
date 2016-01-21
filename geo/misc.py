import operator
from math import sqrt


def digit(num, dig):
    pos = str(num).rfind(".")
    if pos == -1:
        return None
    elif (len(str(num)) - 1 - pos) < dig:
        return None
    return int(str(num)[pos+dig])


def pop_dec(inp, n=6):
    t = []
    for y in range(1, n):
        if type(digit(inp[0], y)) == int and type(digit(inp[1], y)) == int:
            t.append((digit(inp[0], y), digit(inp[1], y)))
        elif type(digit(inp[0], y)) == int and not digit(inp[1], y):
            t.append((digit(inp[0], y), 0))
        elif type(digit(inp[1], y)) == int and not digit(inp[0], y):
            t.append((0, digit(inp[1], y)))
        else:
            t.append((0,0))
    return t

def params(addr):
    prms = {'key': "AIzaSyAgcnAoMCuhgMwXLXwRuGiEZmP0T-oWCRM", 'address': "+".join(addr),
            'lang': 'en'}
    ##  'region': "uk", 'components': "country:GB", 'language': "en"}
    ## region is ccTLD code more info here:
    ## https://en.wikipedia.org/wiki/List_of_Internet_top-level_domains
    ## componenets can be country or two letter country code ISO 3166-1 more info here:
    ## https://en.wikipedia.org/wiki/ISO_3166-1
    ## language is an optional two letter code from following list:
    ## https://developers.google.com/maps/faq#languagesupport
    ## optional parameter
    return prms


def closest(vec, nest):
    s = {}
    for x in nest:
        p = x.lstrip("(").rstrip(")").split(",")
        s[x] = abs(sqrt((int(p[0])**2) + int(p[1])**2) - vec)
    s = sorted(s.items(), key=operator.itemgetter(1))
    return s[0][0]


def repeat(nest, args):
    temp1 = nest
    coords = []
    args2 = []
    for z in args:
        temp1 = temp1.get(z)
        if temp1:
            for y in temp1:
                if 'coords' in temp1[y]:
                    coords += temp1[y]['coords']
                else:
                    args2.append(y)
            coords += repeat(temp1, args2)
    return coords

