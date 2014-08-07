from db import *
from bs4 import BeautifulSoup as BS
import requests

href = "http://www.behindthename.com/names/search.php?terms=strong+mighty+powerful&type=m"

def getterms(href):

	import re
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

	return d1[0].find_all('a', class_=class_is_not_usg)

hrefs = [h['href'] for h in thmcoll.find({}, {'href': 1})]

print parse_theme(hrefs[5])