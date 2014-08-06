from __future__ import unicode_literals
import sqlalchemy as sql
from sqlalchemy import Table, Column, Binary, String, create_engine
from sqlalchemy.engine.url import URL

db = URL(drivername="mysql+pymysql", database='babynames', query={'read_default_file' : '/Users/azirm/.my.cnf', 'read_default_group' : 'python'}))
eng = create_engine(name_or_url=db)
meta = MetaData(bind=eng)
meta.reflect()

