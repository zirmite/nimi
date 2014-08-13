from db import *
from nltk.corpus import wordnet
from nltk.stem import SnowballStemmer
import scipy.sparse as sparse
import cPickle as cP

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

def keyfeat(keywds, tfidf):

	s1 = set()
	for keyw in keywds:
		keyw = keyw.lower()
		keyw = stemkey(keyw)
		allkeys = getsyns(keyw)
		s1 = s1.union(allkeys)

	skeys = set(tfidf.vocabulary_.keys())
	f1 = sparse.csr_matrix((1, len(skeys)))
	skw = skeys.intersection(s1)
	for matchkw in skw:
		f1[0, tfidf.vocabulary_[matchkw]] = 1 

	return f1

fh = open("tfidf.pkl", "rb")
tfidf = cP.load(fh)
keywds = ['russian', 'flower']
f1 = keyfeat(keywds, tfidf)

