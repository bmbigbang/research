# -*- coding: utf-8 -*-
import operator
from math import sqrt
import re


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


def postcode(query):
    # split codes need to be checked for at least two digits
    split_postcodes = re.compile(ur"(?<![\w\.])\w{2,5}[\- ]\w{2,4}(?![\w\.])", flags=re.U|re.I)
    split_postcodes = [i for i in re.findall(split_postcodes, query) if len(re.findall(r'\d', i)) > 1]
    found = " ".join(split_postcodes)
    # num codes need to not be splits
    num_postcodes = re.compile(ur"(?<![\w\.])\d{4,10}(?![\w\.])", flags=re.U)
    num_postcodes = [i for i in re.findall(num_postcodes, query) if found.find(i) == -1]
    found += " ".join(num_postcodes)
    # split type postcodes without delimiter are looked for except the pure number ones
    split_joined_postcodes = re.compile(ur"(?<![\w\.])\w{2}\d{3,6}(?![\w\.])", flags=re.U|re.I)
    split_joined_postcodes = [i for i in re.findall(split_joined_postcodes, query) if found.find(i) == -1]
    return split_postcodes + num_postcodes + split_joined_postcodes


def getlastnest(nest):
    letters = ""
    for x in nest:
        if unicode("*|") in nest[x]:
            letters += x
            return letters
        temp = nest.get(x)
        if not temp:
            continue
        for y in temp:
            if unicode("*|") in temp[y]:
                letters += x+y
                return letters
    return False


