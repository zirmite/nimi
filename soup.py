from __future__ import unicode_literals
from bs4 import BeautifulSoup as BS
import pymongo as pym
import re
from bson.objectid import ObjectId
import sqlalchemy as sql
from sqlalchemy import create_engine, Table, Column, MetaData
from db import *

def parse_name(name):
	qhtml = htmltab.find_one({'name': name})
	html = qhtml['html']
	soup = BS(html)
	usg = [a.string for a in soup.find_all('a', class_='usg')]
	gender = {'fem': False, 'masc': False}
	if soup.find_all('span', class_='fem'):
		gender['fem'] = True
	if soup.find_all('span', class_='masc'):
		gender['masc'] = True

	try:
		tagpro = [d for d in soup.find_all('div', class_='namesub') if d.span.string=='PRONOUNCED:'][0]
		pronunciation = (tagpro.find('span', class_='info').text).split()[0] # just grab the first token
	except:
		pronunciation = None

	try:
		tagother = [d for d in soup.find_all('div', class_='namesub') if d.span.string=='OTHER LANGUAGES:'][0]
		related = set([t.text for t in tagother.find_all('a', class_='ngl')])
	except IndexError:
		related = None

	try:
		dmean = [d for d in soup.find_all('div', class_='nameheading') if re.match('^Meaning', d.string)][0]
		meaning = dmean.next_sibling.next_sibling.text
	except:
		meaning = None

	return {'mean': meaning, 'pro': pronunciation, 'rel': related, 'gdr': gender, 'name': name, 'usg': usg, '_id': qhtml['_id']}

def extract_simple(info):

	lchar = len(info['name'])
	if info['pro'] is not None:
		lsyl = info['pro'].count('-') + 1
	else:
		lsyl = None
	try:
		male = info['gdr']['masc']
		female = info['gdr']['fem']
	except:
		male = False
		female = False

	first = info['name'][0].lower()

	return {'id': info['_id'], 'name': info['name'], 'M': male, 'F': female, 'lchar': lchar, 'lsyl': lsyl, 'first': first}

def getrelated(info):

	if 'rel' in info.keys() and info['rel'] is not None:
		relLD = [None,] * len(info['rel'])
		for i, n2 in enumerate(info['rel']):
			n2 = n2.upper()
			# print n2
			try:
				n2id = htmltab.find_one({'name': n2}, {'_id': 1})['_id']
				relLD[i] = {'id': info['_id'], 'name': info['name'], 'id2': n2id, 'name2': n2}
			except:
				relLD[i] = {'id': info['_id'], 'name': info['name'], 'name2': n2, 'id2': None}
	else:
		return None

	return relLD

def getusage(info):

	if 'usg' in info.keys() and info['usg'] is not None:
		usgLD = [None,] * len(info['usg'])
		for i, u in enumerate(info['usg']):
			usgLD[i] = {'id': info['_id'], 'name': info['name'], 'origin': u}
	else:
		return None

	return usgLD

if __name__=='__main__':
	for ntable, seli in zip(ntables, sels):

		res1 = eng.execute(seli)

		pname = None
		for name, hid in res1.fetchall():

			if pname==name:
				continue

			print 'name: ' + name
			hid = ObjectId(hid)
			info = parse_name(name)
			info['_id'] = hid
			
			if 'rel' in info.keys() and info['rel']:
				info['rel'] = list(info['rel'])
			else:
				info['rel'] = None

			if infotab.find_one({'_id': hid}):
				pname = name[:]
				print "here\n"
				continue

			infotab.insert(info)
			features = extract_simple(info)
			related = getrelated(info)
			usage = getusage(info)
			# print related
			eng.execute(usgins.values(usage))
			eng.execute(numins.values(features))
			eng.execute(relins.values(related))

			pname = name[:]
