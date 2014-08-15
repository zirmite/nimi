from db import *
from nltk.corpus import wordnet
from nltk.stem import SnowballStemmer
import scipy.sparse as sparse
from sklearn.metrics.pairwise import linear_kernel
import cPickle as cP
import operator
import random
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
			synwords.append(lem.name.lower())
	return set(synwords)

def keyfeat(keyw, tfidf):

	s1 = set()
	skeys = set(tfidf.vocabulary_.keys())

	keyw = keyw.lower()
	keyw = stemkey(keyw)
	# allkeys = getsyns(keyw)
	# s1 = s1.union(allkeys)
	s1.add(keyw)
	m1 = s1.intersection(skeys)
	f1 = sparse.csr_matrix((1, len(skeys)))

	if len(m1) > 0:
		for s in list(m1)[:1]:
			# norm = 1 / len(m1)
			f1[0, tfidf.vocabulary_[s]] = 1.0

		return f1

	else:

		return None


def getresults(keywds):
	
	fh = open("tfidf.pkl", "rb")
	tfidf = cP.load(fh)
	tfidf_t = cP.load(fh)
	fh.close()

	fh = open('docs.pkl', 'rb')
	docs = cP.load(fh)
	docD = cP.load(fh)
	docsdata = cP.load(fh)

	# keywds = ['english', 'flower']
	intresults = OrderedDict()
	results = pd.DataFrame()
	tmpname = tabname = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
	tmptab = Table(tmpname, meta, Column('name_id', Binary(12)), Column('score', Float))
	tmptab.create()

	for i, keywd in enumerate(keywds):
		f1 = keyfeat(keywd, tfidf)
		if i==0:
			cosine = linear_kernel(f1, tfidf_t).flatten()
		else:
			cosine += linear_kernel(f1, tfidf_t).flatten()

	related = cosine.argsort()[:(-len(cosine)-1):-1]
	for name in related:
		scorei = cosine[name] / len(keywds)
		insi = tmptab.insert().values(name_id=docD[name]['_id'].binary, score=scorei)
		eng.execute(insi)

	return tmptab

# sort_scores = sorted(results.iteritems(), key=operator.itemgetter(1), reverse=True)
# top100 = [docD[s[0]]['name'] for s in sort_scores]


