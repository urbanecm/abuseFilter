#!/usr/bin/env python

import json
res_file = open('result.json', 'r')
res = res_file.read()
data = json.loads(res)
