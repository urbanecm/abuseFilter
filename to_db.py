#!/usr/bin/env python

import json
j_f = open('result.json', 'r')
j_t = j_f = j_f.read()
j = json.loads(j_t)
ended = j['ended']
saved = j['saved']
together = j['together']
edited = j['edited']
s_f = open('sql.sql', 'w')
s_f.write("use u13367__urbanecmbot;\n")
s_f.write("delete from abuseFilter;\n")
s_f.write("insert into abuseFilter(ended, saved, together, edited) values("+ str(ended)+", "+str(saved) + ", "+ str(together) + ", " + str(edited)+");\n")
s_f.close()
