# -*- coding: utf-8 -*-
import re
import unicodedata
import nltk
import operator
import ujson


def ngram(words, n=1):
    res = []
    for i in range(len(words)-n+1):
        temp = []
        for j in range(n):
            temp.append(words[i+j])
        res.append(temp)
    return res

r = re.compile(r'[\s\n]', flags=re.LOCALE|re.UNICODE)
f = open("langs.txt", "rb")
langs = ujson.load(f)
f.close()

##for i in nltk.corpus.udhr2.fileids():
##    lang = i[:i.rfind(".")]
##    temp = ngram(nltk.corpus.udhr2.raw(i),n=1)
##    res = {}
##    for j in temp:
##        if r.match(j[0]) or j[0] == u'\x92':
##            continue
##        try:
##            temp2 = unicodedata.name(j[0]).split()
##        except:
##            continue
##
##        if temp2[0] not in res:
##            res[temp2[0]] = 1
##        else:
##            res[temp2[0]] += 1
##    ##langs[lang] = sorted(res.items(),key=operator.itemgetter(1),reverse=True)
##    langs[lang] = res


def checkletters(text):
    res2 = {}
    text = ngram(text.decode("utf-8"))
    for i in text:
        if r.match(i[0]):
            continue
        try:
            temp2 = unicodedata.name(i[0]).split()
        except:
            continue
        if temp2[0] not in res2:
            res2[temp2[0]] = 1.0
        else:
            res2[temp2[0]] += 1.0
    res3 = {}
    for charset in res2:
        for lang in langs:
            if charset not in langs[lang]:
                continue
            if float(langs[lang][charset]) > 500:
                tot = sum([float(i[1]) for i in langs[lang].items()])
                if lang in res3:
                    res3[lang] += (res2[charset]/len(text))*(float(langs[lang][charset])/tot)
                else:
                    res3[lang] = (res2[charset]/len(text))*(float(langs[lang][charset])/tot)
    res3 = sorted(res3.items(), key=operator.itemgetter(1), reverse=True)
    return [[i[0],i[1]] for i in res3]

def checklangs(text):
    res = checkletters(text)
    text = ngram(text.decode("utf-8"), n=5)
    for x in range(len(res)):
        cur = ngram(nltk.corpus.udhr2.raw(res[x][0]+u'.txt'), n=5)
        if 'CJK' in langs[res[x][0]]:
            break
        for y in cur:
            for z in text:
                if y == z:
                    res[x][1] += 1
    srtd = [i for i in sorted(res, key=operator.itemgetter(1), reverse=True)]
    if len(srtd) > 0:
        if srtd[0][1] < 1:
            return srtd
        srtd = [i for i in srtd if i[1] > 0.9]
        if srtd[0][1] > 30:
            srtd = [i for i in srtd if i[1] > 25]
        if srtd[0][1] > 10:
            srtd = [i for i in srtd if i[1] > 8]
    return srtd

# text5 = "saya ingin berkelah" ## malayan
# print checklangs(text5)
# text1 = "Попавший в снежную пробку оренбуржец" ##russian
# print checklangs(text1)
# text2 = "把百度设为主页把百度设为主页关于百度" ## chinese
# print checklangs(text2)
# text3 = "this isn't english"
# print checklangs(text3)
# text4 = "dieses nicht Deutsch" ## german
# print checklangs(text4)
# text6 = "หน้าแรก ได้จากโฮมเพจ เกี่ยวกับ"
# print checklangs(text6)  ## japanese
# text7 = "ホームページについてホームページ"
# print checklangs(text7)
# text8 = "சாவிகளைத் தொலைத்துவிட்டேன்" ## TAMIL
# print checklangs(text8)
# text9 = "मेरी चाबियां खो गई हैं" ## hindi
# print checklangs(text9)

