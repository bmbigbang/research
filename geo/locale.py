# -*- coding: utf-8 -*-
import re
import locale
from langdetect import checklangs
test2 = """٠١٢٣٤٥ مرحبا انا  البشري """
test3 = u"\u0661\u0660"
test2 += " 1354123"
locale.setlocale(locale.LC_ALL, str(checklangs(test2)[0][0]))
print locale.getlocale()
pattern = re.compile(ur"\d+", flags=re.U)
print re.findall(pattern, test2.decode("utf-8"))
locale.setlocale(locale.LC_ALL, "eng")
print locale.getlocale()

test4 = "北京东城区东直门内大街号奇门涮肉坊(簋街总店)对面".decode("utf-8")
pattern = re.compile(ur"\p{Z}+", flags=re.U)
print re.findall(pattern, test4)

