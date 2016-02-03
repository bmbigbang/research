import pint
import re

unitdict = {
    "thou\'s": "thou",
    "inch\'s": "inch",
    "ins": "inch",
    "in\'s": "inch",
    "\"": "inch",
    "foot": "foot",
    "yard\'s": "yard",
    "yrd": "yard",
    "yrds": "yard",
    "yrd\'s": "yard",
    "convert": "to",
    "change": "to",
    "in": "to"
}

ureg = pint.UnitRegistry()


def convert(query):
    query = query.decode("utf-8")
    pattern = re.compile(ur"[a-z]*", flags=re.U|re.I)
    for x in re.findall(pattern, query):
        if x in unitdict:
            query = query.replace(x, unitdict[x])

    pattern = re.compile(ur"\b\S*\d[\s\-]?[a-z]\S*\b", flags=re.U|re.I)
    frm = re.search(pattern, query)
    frm = query[frm.start():frm.end()]
    frmdgts = float(u"".join([i.replace(u",", u"") for i in frm if i.isdigit() or i in u",."]))
    frmunits = u"".join([i for i in frm if i.isalpha()])
    conv = query.replace(frm, u"").replace(u"to", u"").strip()
    try:
        frm = frmdgts * ureg[frmunits]
    except pint.unit.UndefinedUnitError:
        return "from unit error: " + str(pint.unit.UndefinedUnitError)
    try:
        return frm.to(ureg[conv])
    except pint.unit.UndefinedUnitError:
        return "from/to unit error: " + str(pint.unit.UndefinedUnitError)
    except pint.unit.DimensionalityError:
        return "from/to units are different types: " + str(pint.unit.DimensionalityError)


testinput = "24yrds to m"
print testinput + " => " + str(convert(testinput))
testinput = "24 miles to m"
print testinput + " => " + str(convert(testinput))
testinput = "24-miles in m"
print testinput + " => " + str(convert(testinput))
testinput = "24.2-miles to m"
print testinput + " => " + str(convert(testinput))
testinput = "24,2-miles convert m"
print testinput + " => " + str(convert(testinput))
testinput = "5-kg convert km"
print testinput + " => " + str(convert(testinput))

