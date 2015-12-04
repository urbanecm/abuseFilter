#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json

out_file = open('output.out', 'r')
out = out_file.read()
out = json.loads(out)

result = ""
result += "['Editace ukončena', " + str(out['ended']) + "],\n"
result += "['Editace uložena', " + str(out['saved']) + "],\n"
result += "['Editace upravena', " + str(out['edited']) + "]"
print result
