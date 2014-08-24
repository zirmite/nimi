from db import *
from sqlalchemy.sql.expression import Executable, ClauseElement
from sqlalchemy.ext import compiler

class InsertFromSelect(Executable, ClauseElement):
    def __init__(self, table, select):
        self.table = table
        self.select = select

@compiler.compiles(InsertFromSelect)
def visit_insert_from_select(element, compiler, **kw):
 return "INSERT INTO %s %s" % (
     compiler.process(element.table, asfrom=True),
     compiler.process(element.select)
)

ranktab = meta.tables['ranking']
colone = sql.sql.expression.literal_column("1")
colzero = sql.sql.expression.literal_column("0")
# populate ranking table
# doing this by hand with a counting variable

# define metrics
# popular
# insert into popular (name_id, popular) select name_id, 1 from (select name_id from ranking where rank <= 25 and year > 2003 group by name_id having count(rank) >= 1) as r;
selpop = sql.select([ranktab.c.name_id.label('name_id'), colone.label('popular'), colzero.label('notpopular'), colzero.label('unusual'), colzero.label('rare')]).where(and_(ranktab.c.rank <= 25, ranktab.c.year >= 2003)).group_by(ranktab.c.name_id).having(sql.func.count(ranktab.c.rank) >= 1)
poptab = meta.tables['popular']
inspop = InsertFromSelect(poptab, selpop)

selnotpop = sql.select([ranktab.c.name_id, 1]).where(and_(ranktab.c.rank > 25, ranktab.c.rank <= 100, ranktab.c.year >= 2003)).group_by(ranktab.c.name_id).having(sql.func.count(ranktab.c.rank) >= 1)
InsertFromSelect(poptab, selnotpop)

selunu = sql.select([ranktab.c.name_id, 1]).where(and_(ranktab.c.rank > 100, ranktab.c.year >= 2003)).group_by(ranktab.c.name_id).having(sql.func.count(ranktab.c.rank) >= 1)
InsertFromSelect(poptab, selunu)

