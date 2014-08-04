from __future__ import unicode_literals
import requests
from bs4 import BeautifulSoup as BS
import re
import sqlalchemy as sql
from sqlalchemy import Table, String, Column, MetaData
from dbcode.db.conn import *
import time
import numpy.random as nrand

db.database = 'babynames'
eng = sql.create_engine(name_or_url=db)
meta = MetaData(bind=eng)

baseurl = "http://www.behindthename.com/names/gender/masculine"
baseurl = "http://www.behindthename.com/names/gender/feminine"
nameurl = "http://www.behindthename.com"

# soup = BS(requests.get(baseurl).content)
# allas = soup.find_all('a')
# nre = re.compile("^/name/")
# allnametags = [a for a in allas if nre.match(a.attrs['href']) and 'class' not in a.attrs]
# allnames = [a.text for a in allnametags]
# allhrefs = [a.attrs['href'] for a in allnametags]
# for x in xrange(2,37):
# 	soupi = soup = BS(requests.get(baseurl+'/'+str(x)).content)
# 	allasi = soup.find_all('a')
# 	allnametagsi = [a for a in allasi if nre.match(a.attrs['href']) and 'class' not in a.attrs]
# 	allnamesi = [a.text for a in allnametagsi]
# 	allhrefsi = [a.attrs['href'] for a in allnametagsi]
# 	allhrefs.extend(allhrefsi)
# 	allnames.extend(allnamesi)

# boynames = Table("girlnames", meta, Column("name", String(50)), Column("href", String(50)))
# meta.create_all()
# eng.execute(boynames.delete())
# dlist = [{'name': k, 'href': l} for k, l in zip(allnames, allhrefs)]
# eng.execute(boynames.insert(), dlist)

meta.reflect()
boynames = meta.tables['boynames']
sel1 = sql.select([boynames.c.name])
allnames = eng.execute(sel1).fetchall()

apiurl = "https://www.kimonolabs.com/api/2weld18y?apikey=yexwWpC23aIIu1DTXwMiqouzr0oeVFWz"
jsontot = {}
unire = re.compile("\d|\W")
for i, (name, href) in enumerate(allnames): # nrand.choice(allnames, 50)):
	while unire.search(name):
		name, href = random.choice(allnames)
	urli = apiurl + '&kimpath2=' + name
	nameurli = nameurl + href
	rawname = requests.get(nameurli)
	response = requests.get(urli)
	conti = None
	if response.status_code == 200:
		conti = response.json()['results']['collection1'][0]
	else:
		conti = {'name': name}
	jsontot[name] = conti
	print str(i) + ": " + name
	# time.sleep(1)