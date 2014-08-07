from __future__ import unicode_literals
import sqlalchemy as sql
from sqlalchemy import Table, Column, Binary, String, Boolean, MetaData, create_engine, Integer, and_
from sqlalchemy.engine.url import URL
import pymongo as pym

client = pym.MongoClient()
dbm = client.names
htmltab = dbm.html
infotab = dbm.info
thmcoll = dbm.themes
assocoll = dbm.assoc

dbsql = URL(drivername="mysql+pymysql", database='babynames', query={'read_default_file' : '/Users/azirm/.my.cnf', 'read_default_group' : 'python', 'use_unicode': 1, 'charset': 'utf8'})
eng = create_engine(name_or_url=dbsql)
meta = MetaData(bind=eng)
meta.clear()
meta.reflect()

boynames = meta.tables['boynames']
girlnames = meta.tables['girlnames']
ntables = [boynames, girlnames]
sels = [sql.select([ntable.c.name, ntable.c.htmlid]).where(ntable.c.htmlid!=None) for ntable in ntables]

if 'names' not in meta.tables:
	numtab = Table("names", meta, Column('id', Binary(12)), Column('name', String(50)), Column('M', Boolean), Column('F', Boolean), Column('lchar', Integer), Column('lsyl', Integer), Column('first', String(1)))
	meta.create_all()
else:
	numtab = meta.tables['names']

if 'related' not in meta.tables:
	reltab = Table("related", meta, Column('id', Binary(12)), Column('name', String(50)), Column('id2', Binary(12)), Column('name2', String(50)))
	meta.create_all()
else:
	reltab = meta.tables['related']

if 'usages' not in meta.tables:
	usgtab = Table("usages", meta, Column('id', Binary(12)), Column('name', String(50)), Column('origin', String(50)))
	meta.create_all()
else:
	usgtab = meta.tables['usages']

if 'themes' not in meta.tables:
	thmtab = Table("themes", meta, Column('id', Binary(12)), Column('name', String(50)), Column('theme', String(50)))
	meta.create_all()
else:
	thmtab = meta.tables['themes']

if 'assoc' not in meta.tables:
	assoctab = Table("assoc", meta, Column('id', Binary(12)), Column('name', String(50)), Column('assoc', String(50)))
	meta.create_all()
else:
	assoctab = meta.tables['assoc']


numins = numtab.insert()
numq = numtab.select()
relins = reltab.insert()
usgins = usgtab.insert()


