from db import *
from nltk.corpus import wordnet
from nltk.stem import SnowballStemmer
import nltk
import scipy.sparse as sparse
from sklearn.metrics.pairwise import linear_kernel
import cPickle as cP
import operator
import random
import os
import pandas as pd
import string
import numpy as np
from sqlalchemy import PrimaryKeyConstraint, Index
from collections import OrderedDict

def stemkey(word):
	stemmer = SnowballStemmer('english')
	return stemmer.stem(word)

def getsyns(word):
	synwords = []
	syns = wordnet.synsets(word)
	for syn in syns:
		l = syn.lemmas
		for lem in l:
			syni = lem.name.lower()
			syni = syni.replace("_", " ")
			synwords.append(syni)
	return set(synwords)

def keyfeat(keyw, tfidf, tfidf_t, names):

	s1 = set()
	skeys = set(tfidf.vocabulary_.keys())
	f1 = sparse.csr_matrix((1, len(skeys)))

	keyw = keyw.lower()
	# selname = sql.select([numtab.c.id]).where(numtab.c.name==keyw.upper()).limit(1)
	# rname = eng.execute(selname)
	if keyw in names:
		# objid = ObjectId(rname.fetchone()[0])
		nameind = names.index(keyw) 
		return tfidf_t[nameind, :]
		
		
	if keyw not in skeys:
		keyw = stemkey(keyw)

	s1.add(keyw)
	m1 = s1.intersection(skeys)

	if len(m1) > 0:
		for s in list(m1)[:1]:
			# norm = 1 / len(m1)
			# f1[0, tfidf.vocabulary_[s]] = 1.0
			f1 = tfidf.transform(s)

		return f1

	else:

		return f1


def getresults(keywds):
	
	fh = open(os.path.abspath('../') + "/tfidf.pkl", "rb")
	tfidf = cP.load(fh)
	tfidf_t = cP.load(fh)
	fh.close()

	fh = open(os.path.abspath('../') + '/docs.pkl', 'rb')
	docs = cP.load(fh)
	docD = cP.load(fh)
	docsdata = cP.load(fh)

	names = [None,] * len(docD.keys())
	for i in docD.keys():
		names[i] = docD[i]['name'].lower()

	intresults = OrderedDict()
	results = pd.DataFrame()
	tmpname = tabname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
	tmptab = Table(tmpname, meta, Column('name_id', Binary(12)), Column('name', String(50)), Column('score', DOUBLE), Column('mean', String(500)), Index('id', "name_id", unique=True, mysql_length=12), Index('name', 'name', unique=True))

	tmptab.create()

	keywds.extend([' '.join(x) for x in nltk.bigrams(keywds)])
	keywdsyn = keywds[:]
	# for key in set(keywds):
	# 	syns = getsyns(key)
	# 	keywdsyn.extend(list(syns))

	f1 = sparse.csr_matrix((1, tfidf_t.shape[1]))
	for i, keywd in enumerate(keywdsyn):

		f1 = f1 + keyfeat(keywd, tfidf, tfidf_t, names)
		# print keywd
		# if i==0 and f1 is not None:
		# 	cosine = linear_kernel(f1, tfidf_t).flatten()
		# elif f1 is not None:
		# 	cosine += linear_kernel(f1, tfidf_t).flatten()

	cosine = linear_kernel(f1, tfidf_t).flatten()
	related = cosine.argsort()[:-1000:-1]
	for name in related:
		scorei = cosine[name] #/ len(keywds)
		# scorei += np.random.normal(0.0, scorei / 10.0)

		try:
			meani = infotab.find_one({'_id': docD[name]['_id']})['mean']
			# meani = meani.replace('"', '&quot;')
		except:
			meani = ''

		if scorei > 0.001:
			try:
				insi = tmptab.insert().values(name_id=docD[name]['_id'].binary, score=float(scorei), mean=meani, name=docD[name]['name'])
				eng.execute(insi)
			except:
				pass

	return tmptab

# sort_scores = sorted(results.iteritems(), key=operator.itemgetter(1), reverse=True)
# top100 = [docD[s[0]]['name'] for s in sort_scores]

if __name__ == '__main__':
	tmptab = getresults(['welsh', 'mythology', 'sea'])
	tmptab.drop()
