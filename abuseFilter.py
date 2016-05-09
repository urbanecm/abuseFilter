#!/usr/bin/env python
#-*- coding: utf-8 -*-

#############################################################
#TODO: Zajistit, aby program pracoval i se smazanými revizemi (z tabulky archive)

############################ INIT ####################################
#Importování modulů
#Importování modulu pro práci s výstupem ve formátu JSON
import json
#Importování modulu pro práci s objekty spravovanými interpretem
import sys
#Importování knihovny pro práci s databází
from wmflabs import db
#Importování modulu pro práci s datem a časem
import datetime

#Init modulů
#Vytvoření proměnné s kódem wikiprojektu
#wikisite = sys.argv[1] + "wiki"
wikisite = "cswiki"
#Vytvoření proměnné s číslem filtru
#fnum = sys.argv[2]
fnum = 15
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
#Vytvoření pomocných proměnných
pageDeleted = 0
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
				#Jestliže byla stránka smazána, nastav tak rev_near
				rev_near = [["DeletedPage"]]
			else:
				#Pokud ne, zjisti, zda kolem spuštění filtru proběhla nějaká editace
				cur = conn.cursor()
				with cur:
					cur.execute('select * from revision where rev_page=(select page_id from page where page_namespace=0 and page_title="' + group[0][10] + '" limit 1) order by rev_timestamp asc')
					data = cur.fetchall()
				#Převést na datetime objekt
				stamp = group[0][8]
				stampDt = datetime.datetime.strptime(stamp,'%Y%m%d%H%M%S')
				stamp = stampDt
				del(stampDt)
				for rev in data:
					#Převést data v tabulce na datetime objekt
					stamp2 = datetime.datetime.strptime(rev[6], '%Y%m%d%H%M%S')
					#Hledáme blízké revize, dokud je timestamp menší, přeskakuj
					if stamp2.year < stamp.year:
						continue
					elif stamp2.month < stamp.month:
						continue
					elif stamp2.day < stamp.day:
						continue
					elif stamp2.hour < stamp.hour:
						continue
					elif stamp2.minute < stamp.minute:
						continue
					elif stamp2.second < stamp.second:
						continue
					#Dorazili jsme na alespoň stejně datovanou revizi
					#Přičti k timestamp u abuseFilteru 15 sekund
					stampA = stamp + datetime.timedelta(0, 15)
					#Jakmile najdeme mladší revizi, přidejme ji do proměnné, pokud je starší, stopni cyklus
					if stamp2.year < stampA.year:
						rev_near.append(rev)
					elif stamp2.month < stampA.month:
						rev_near.append(rev)
					elif stamp2.day < stampA.day:
						rev_near.append(rev)
					elif stamp2.hour < stampA.hour:
						rev_near.append(rev)
					elif stamp2.minute < stampA.minute:
						rev_near.append(rev)
					elif stamp2.second < stampA.second:
						rev_near.append(rev)
					else:
						break
		#Jestliže žádná editace kolem spuštění neproběhla, editra varování zastrašilo
			if len(rev_near) == 0:
				ended += 1
				together += 1
			else:
				#Jestli ne, zjisti, zda nebyla stránka smazána
				if rev_near[0][0] == "DeletedPage":
					#Pokud ano, zvyš počitadlo
					pageDeleted += 1
					together += 1
				else:
					#Pokud ne, editr editaci upravil, aby prošla filtrem
					edited += 1
					together += 1
		else:
			#Pokud se nejednalo hned o varování, musela být editace uložena
			saved += 1
			together += 1
	else:
		#Pokud se k jedné stránce vztahuje více logů, musela být editace uložena
		saved += 1
		together += 1

#Vytištění výsledků na výstup
result = {}
result['saved'] = saved
result['ended'] = ended
result['edited'] = edited
result['pageDeleted'] = pageDeleted
result['together'] = together
o_f = open('result.json', 'w')
o_f.write(json.dumps(result))
print json.dumps(result)
