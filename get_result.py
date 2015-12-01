#!/usr/bin/env python
#-*- coding: utf-8 -*-

#Importování modulu pro práci s objekty spravovanými interpretem
import sys
#Vytvoření proměnné s kódem wikiprojektu
#wikisite = sys.argv[1] + "wiki"
wikisite = "cswiki"
#Vytvoření proměnné s číslem filtru
#fnum = sys.argv[2]
fnum = 15
#Importování knihovny pro práci s databází
from wmflabs import db
#Navázání připojení s databází
conn = db.connect(wikisite)

#Vytvoření databázové transakce
cur = conn.cursor()
#Otevření transakce
with cur:
	#Nalezení ĺogu pro daný filtr
	cur.execute('select afl_actions from abuse_filter_log where afl_filter="' + str(fnum) + '"order by afl_timestamp asc')
	data = cur.fetchall()

import json
print json.dumps(data)
