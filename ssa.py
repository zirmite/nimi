from db import *
import glob
import re
import pandas as pd

yre = re.compile("yob(\d\d\d\d).txt")
files = [str(y) for y in glob.glob("../data/namesSSA/yob*.txt") if int(yre.search(y).group(1)) < 1940]

for file in files:
	year = int(yre.search(file).group(1))
	dfi = pd.read_csv(file, names=['name', 'gdr', 'n'])
	rows = [{'name': r[1]['name'], 'n': r[1]['n'], 'gdr': r[1]['gdr'], 'year': year} for r in dfi.iterrows()]
	insall = ssatab.insert().values(rows)
	eng.execute(insall)