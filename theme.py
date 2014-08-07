from db import *
from bs4 import BeautifulSoup as BS
from bson.objectid import ObjectId
import requests
import re

def getterms(href):

	import string
	tre = re.compile("terms=(.+?)\&")

	baseurl = 'http://www.behindthename.com/names/meaning/'

	try:
		return baseurl + string.join(tre.search(href).group(1).split('+'), ',')
	except:
		return None

def parse_theme(href):

	print getterms(href)
	html = requests.get(getterms(href)).content
	soup = BS(html)
	d1 = soup.find_all('div', class_='browsename')

	def class_is_not_usg(cssclass):
		return cssclass != 'usg'

	try:
		return [d.find_all('a', {'href': re.compile('^/name/')})[0] for d in d1]
	except Exception as e:
		print e
		return None

if __name__=="__main__":

	recs = [r for r in thmcoll.find({}, {'href': 1, 'text': 1})]
	orecs = [r for r in assocoll.find({}, {'href': 1, 'text': 1})]
	hrefs = [h['href'] for h in recs]
	texts = [re.sub('"', '', h['text']) for h in recs]

	for i, (href, text) in enumerate(zip(hrefs, texts)):
		names = parse_theme(href)

		for j, name in enumerate(names):
			nref = name.attrs['href']
			name = name.text
			objids = htmltab.find({'name': name}, {'_id': 1})

			try:
				thmins = thmins.values({'id': objids[0]['_id'], 'name': name, 'theme': text})
				eng.execute(thmins)
			except:
				pass



