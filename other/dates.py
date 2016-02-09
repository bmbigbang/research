# -*- coding: utf-8 -*-

import dateparser
import datetime
import re
import itertools


def parse(date):
    results = []
    date = date.replace(u',', u'').split()
    for x in range(len(date), 0, -1):
        for y in itertools.combinations(date, x):
            if dateparser.parse(u" ".join(y)):
                return dateparser.parse(u" ".join(y))
    return results


testinput = u"July 4, 2013 foo bar"
print testinput + u" => " + unicode(parse(testinput))
testinput = u'foo bar Le 11 Décembre 2014 à 09:00'
print testinput + u" => " + unicode(parse(testinput))
testinput = u'Le 11 Décembre foo bar 2014 à 09:00'
print testinput + u" => " + unicode(parse(testinput))
testinput = u'13 foo января 2015 г. в 13:34 bar'
print testinput + u" => " + unicode(parse(testinput))


