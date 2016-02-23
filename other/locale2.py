# -*- coding: utf-8 -*-
import re
import locale
from langdetect import checklangs
test2 = """٠١٢٣٤٥ مرحبا انا  البشري """
test3 = u"\u0661\u0660"
test2 += " 1354123"
# set locale resources for windows 10:
# https://msdn.microsoft.com/en-us/library/cdax410z(VS.71).aspx
# https://msdn.microsoft.com/en-us/library/39cwe7zf(vs.71).aspx
# setting locale changes the string.letters loaded through string
locale.setlocale(locale.LC_ALL, str(checklangs(test2)[0][0]))
print locale.getlocale()
pattern = re.compile(ur"\d+", flags=re.U|re.L)
print re.findall(pattern, test2.decode("utf-8"))
locale.setlocale(locale.LC_ALL, "eng")
print locale.getlocale()

pattern = re.compile(ur"\d+", flags=re.U|re.L)

print re.findall(pattern, test2)

