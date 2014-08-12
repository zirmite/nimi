import nltk
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
import gensim
import string
import re
from db import *

from nltk.corpus import stopwords
stopw = stopwords.words('english')
stopw.extend(['name', 'word', 'surname', 'meaning', 'history', 'born', 'originally', 'means'])
# stopw.extend([n['name'].lower() for n in infotab.find({}, {'name': 1})])
stopw.extend(list(string.letters.lower()))
stopw = set(stopw)
tok1 = RegexpTokenizer("\w+")
upper_re = re.compile('\W([A-Z]+?)\W')

docs = []
docD = {}
i = 1
for name in infotab.find({}):
	if name['mean'] is not None:
		if upper_re.search(name['mean']):
			# print name['name'] + '\n'
			# print name['mean'] + '\n'
			# print upper_re.search(name['mean']).group(1)
			try:
				relname = infotab.find_one({'name': upper_re.search(name['mean']).group(1)})
				name['mean'] += ' ' + relname['mean']
			except:
				pass
		wi = [w for w in tok1.tokenize(name['mean'].lower()) if w not in stopw]
		numw = len(wi)
		if numw < 15:
			continue
		else:
			ddir = {'name': name['name'], '_id': name['_id']}

			if name['rel'] is not None:
				ddir['nrel'] = len(name['rel'])
			else:
				ddir['nrel'] = 0

			docs.append(wi)
			docD[i] = ddir
			i += 1
	else:
		continue

docsdata = [string.join(d) for d in docs]
tfidf = TfidfVectorizer(max_features=200, use_idf=True, sublinear_tf=True, ngram_range=(1,3), max_df=0.7).fit(docsdata)
# f = open("/Users/azirm/Documents/insight/babynames/malletin/docs.txt", "w")
# for doc in docs:
# 	f.write(string.join(doc))
# 	f.write("\n")

# f.close()