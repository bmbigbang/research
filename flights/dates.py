# -*- coding: utf-8 -*-
import dateparser
import datetime
print datetime.datetime(dateparser.parse(u'1 เดือนตุลาคม 2005, 1:00 AM'))
print datetime.datetime(dateparser.parse(u'15 mar 12'))
