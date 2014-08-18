import nltk
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
import gensim
import string
import re
import os.path
import cPickle as cP
from bson.objectid import ObjectId
from db import *

objidsel = sql.select([hreftab.c.href]).where(hreftab.c.name_id==bindparam('objid'))

from nltk.corpus import stopwords
stopw = stopwords.words('english')
stopw.extend(['name', 'word', 'surname', 'meaning', 'history', 'born', 'originally', 'means'])
# stopw.extend([n['name'].lower() for n in infotab.find({}, {'name': 1})])
stopw.extend(list(string.letters.lower()))
stopw = set(stopw)
tok1 = RegexpTokenizer("\w+")
upper_re = re.compile('\W([A-Z]+?)\W')

def getthms(name, relname=None):

	if relname is not None:
		selthm = sql.select([thmtab.c.theme_name]).where(and_(or_(nthmtab.c.id==name['_id'].binary, nthmtab.c.id==relname['_id'].binary), nthmtab.c.theme_id==thmtab.c.theme_id))
	else:
		selthm = sql.select([thmtab.c.theme_name]).where(and_(nthmtab.c.id==name['_id'].binary, nthmtab.c.theme_id==thmtab.c.theme_id))

	rthm = eng.execute(selthm)

	thmstr = string.join([t for t in rthm.fetchall()])
	return thmstr

pklf = "docs.pkl"
remake = False
if (not os.path.isfile(pklf)) or (remake):
	docs = []
	docD = {}
	i = 0
	selnames = sql.select([numtab.c.id.distinct()])
	rnames = eng.execute(selnames)
	for nid in rnames.fetchall():
		name = infotab.find_one({'_id': ObjectId(nid[0])})
		if name['mean'] is not None:

			if upper_re.search(name['mean']):

				try:
					relname = infotab.find_one({'name': upper_re.search(name['mean']).group(1)})
					name['mean'] += ' ' + relname['mean']
					thms = getthms(name, relname)
				except:
					pass

			thms = getthms(name)
			name['mean'] += thms
			wi = [w for w in tok1.tokenize(name['mean'].lower()) if w not in stopw]
			numw = len(wi)
			if numw < 1:
				continue
			else:
				ddir = {'name': name['name'], '_id': name['_id']}
				rhref = eng.execute(objidsel, objid=name['_id'].binary)
				ddir['href'] = rhref.fetchone()[0]

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
	fh = open(pklf, 'wb')
	cP.dump(docs, fh, protocol=-1)
	cP.dump(docD, fh, protocol=-1)
	cP.dump(docsdata, fh, protocol=-1)
	fh.close()

else:
	fh = open(pklf, 'rb')
	docs = cP.load(fh)
	docD = cP.load(fh)
	docsdata = cP.load(fh)
	fh.close()

tfidf = TfidfVectorizer(max_features=2000, use_idf=True, sublinear_tf=False, ngram_range=(1,2), max_df=0.95).fit(docsdata)
fh = open('tfidf.pkl', 'wb')
tfidf_t = tfidf.transform(docsdata)
cP.dump(tfidf, fh, protocol=-1)
cP.dump(tfidf_t, fh, protocol=-1)
fh.close()
# f = open("/Users/azirm/Documents/insight/babynames/malletin/docs.txt", "w")
# for doc in docs:
# 	f.write(string.join(doc))
# 	f.write("\n")

# f.close()