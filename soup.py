from __future__ import unicode_literals
from bs4 import BeautifulSoup as BS
import pymongo as pym
import re
from bson.objectid import ObjectId

client = pym.MongoClient()
dbm = client.names
htmltab = dbm.html


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

	return {'mean': meaning, 'pro': pronunciation, 'rel': related, 'gdr': gender, 'name': name, 'usg': usg}

name = 'ANDREW'
# name = 'ANDER'
# name = 'GWEN'
# name = 'WILLIS'

info = parse_name(name)
