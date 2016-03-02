#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json

f = open('result.json', 'r')
data = json.loads(f.read())

res = []
res.append('["Ukončeno", ' + str(data['ended']) + '],')
res.append('["Uloženo", ' + str(data['saved']) + '],')
res.append('["Upraveno", ' + str(data['edited']) + ']')
for i in res:
	print i
