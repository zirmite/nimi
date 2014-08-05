from bs4 import BeautifulSoup as BS
import pymongo as pym
from bson.objectid import ObjectId

client = pym.MongoClient()
dbm = client.names
htmltab = dbm.html

name = 'ANDREW'
html = htmltab.find_one({'name': name})['html']

soup = BS(html)
usg = [a.string for a in soup.find_all('a', class_='usg')]
gender = {'fem': False, 'masc': False}
if soup.find_all('span', class_='fem'):
	gender['fem'] = True
if soup.find_all('span', class_='masc'):
	gender['masc'] = True

