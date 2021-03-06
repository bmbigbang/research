# -*- coding: utf-8 -*-

import binascii

gsm = ("@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞ\x1bÆæßÉ !\"#¤%&'()*+,-./0123456789:;<=>?"
       "¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ`¿abcdefghijklmnopqrstuvwxyzäöñüà")
ext = ("````````````````````^```````````````````{}`````\\````````````[~]`"
       "|````````````````````````````````````€``````````````````````````")

def gsm_encode(plaintext):
    result = []
    for c in plaintext:
        idx = gsm.find(c)
        if idx != -1:
            result.append(chr(idx))
            continue
        idx = ext.find(c)
        if idx != -1:
            result.append(chr(27) + chr(idx))
    return ''.join(result).encode('hex')

def gsm_decode(hexstr):
    res = hexstr.decode('hex')
    res = iter(res)
    result = []
    for c in res:
        if c == chr(27):
            c = next(res)
            result.append(ext[ord(c)])
        else:
            result.append(gsm[ord(c)])
    return ''.join(result)

code = gsm_encode("Hello World {}")
print(code)
# 64868d8d903a7390938d853a1b281b29
print(gsm_decode(code))
# Hello World {}
print "A" == (gsm_decode(gsm_encode(chr(65))))
print '\x1b' == gsm_decode(gsm_encode(chr(27)))