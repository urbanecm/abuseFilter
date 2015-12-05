#!/usr/bin/env python
#-*- coding: utf-8 -*-

############################ INIT ####################################
#Importování modulu pro práci s výstupem ve formátu JSON
import json
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

######################### ZÍSKÁVÁNÍ DAT ###############################

#Vytvoření databázové transakce
cur = conn.cursor()
#Otevření transakce
with cur:
	#Nalezení ĺogu pro daný filtr
	cur.execute('select * from abuse_filter_log where afl_filter="' + str(fnum) + '"order by afl_timestamp asc')
	data = cur.fetchall()


###################### TŘÍDĚNÍ DAT ###############################

#Vytovření proměnné pro roztříděná data
for_analyze = []
#´Vytvoření pomocných proměnných
prevs = []
prev_article = u"wqshnhaAQJHADKJHFGUIA"
for row in data:
	#Je název článku shodný s předchozím?
	if row[10] == prev_article:
		#Přidej ho do pomocné proměnné
		prevs.append(row)
	else:
		#Přidej do roztříděných dat tento a předchozí. 
		prevs.append(row)
		for_analyze.append(prevs)
		#Vyprázdni předchozí
		prevs = []
	#Aktualizuj předchozí název článku
	prev_article = row[10]

#Smazání nepotřebných pomocných proměnných
del(prev_article)
del(prevs)

import json
r_file = open('result.json', 'w')
r_file.write(json.dumps(for_analyze))

"""
#Vytvoření pomocných proměnných
saved = 0
ended = 0
edited = 0
together = 0


################### ANALYZOVÁNÍ DAT ########################

for group in for_analyze:
	if len(group) == 1:
		if group[0][6] == "warn":
			cur = conn.cursor()
			with cur:
				cur.execute('select page_id from page where page_title="' + group[0][10] + '"')
				data = cur.fetchall()
			rev_near = []
			if len(data) == 0:
				rev_near = []
			else:
				cur = conn.cursor()
				with cur:
					cur.execute('select * from revision where rev_page=(select page_id from page where page_namespace=0 and page_title="' + group[0][10] + '" limit 1) order by rev_timestamp asc')
					data = cur.fetchall()
				stamp = int(group[0][8])
				for rev in data:
					if rev[6] < stamp:
						continue
					elif rev[6] > stamp+15:
						break
					else:
						rev_near.append(rev)
			if len(rev_near) == 0:
				ended += 1
				together += 1
			else:
				edited += 1
				together += 1
		else:
			saved += 1
			together += 1
	else:
		saved += 1
		together += 1

#Vytištění výsledků na výstup
result = {}
result['saved'] = saved
result['ended'] = ended
result['edited'] = edited
result['together'] = together
print json.dumps(result)
"""
