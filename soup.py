from bs4 import BeautifulSoup as BS
import pymongo as pym
from bson.objectid import ObjectId

client = pym.MongoClient()
dbm = client.names
htmltab = dbm.html

name = 'WILLIS'
html = htmltab.find_one({'name': name})['html']

soup = BS(html)
usg = [a.string for a in soup.find_all('a', class_='usg')]
gender = {'fem': False, 'masc': False}
if soup.find_all('span', class_='fem'):
	gender['fem'] = True
if soup.find_all('span', class_='masc'):
	gender['masc'] = True

tagpro = [d for d in soup.find_all('div', class_='namesub') if d.span.string=='PRONOUNCED:'][0]
pronunciation = (tagpro.find('span', class_='info').text).split()[0] # just grab the first token

try:
	tagother = [d for d in soup.find_all('div', class_='namesub') if d.span.string=='OTHER LANGUAGES:'][0]
	related = set([t.text for t in tagother.find_all('a', class_='ngl')])
except IndexError:
	related = set()