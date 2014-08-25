from flask import render_template
from flask import jsonify, request
from app import app
import pymysql as mdb
import sys, os

sys.path.append(os.path.abspath('../'))
from namequery import *

db = mdb.connect(user="root", host="localhost", db="babynames",
charset='utf8', unix_socket="/opt/local/var/run/mysql55/mysqld.sock")

@app.route('/')
@app.route('/index')
def index():
    return render_template("index_gray.html")

@app.route('/jquery')
def index_jquery():
    return render_template('index_gray.html')

@app.route("/db_json")
def db_json():
    keywords = request.args.get('keywords')
    male = request.args.get('male')
    female = request.args.get('female')
    pop = request.args.get('pop')
    notpop = request.args.get('notpop')
    unu = request.args.get('unu')
    rare = request.args.get('rare')
    # print request.form
    keywords = keywords.split()
    # print male, female
    # print request.method
    gdrwhere = (sql.sql.expression.literal_column("1")==1)
    if male=='true':
        gdrwhere = and_(numtab.c.M==1)
    if female=='true':
        gdrwhere = and_(numtab.c.F==1)

    if male=='true' and female=='true':
        gdrwhere = or_(numtab.c.M==1, numtab.c.F==1)

    popid = (poptab.c.name_id==numtab.c.id)
    popwhere = None
    if pop=='true':
        popwhere = and_(poptab.c.popular==1)
    if notpop=='true':
        if popwhere is not None:
            popwhere = or_(popwhere, poptab.c.notpopular==1)
        else:
            popwhere = (poptab.c.notpopular==1)
    if unu=='true':
        if popwhere is not None:
            popwhere = or_(popwhere, poptab.c.unusual==1)
        else:
            popwhere = (poptab.c.unusual==1)

    if popwhere is None or rare=='true':
        popwhere = (sql.sql.expression.literal_column("1")==1)
    # with db:
    tmptab = getresults(keywords) 
    seli = sql.select([numtab.c.name, hreftab.c.href, tmptab.c.mean, tmptab.c.score]).where(and_(tmptab.c.name_id==numtab.c.id, tmptab.c.name_id==hreftab.c.name_id)).group_by(numtab.c.name).order_by(tmptab.c.score.desc())
    seli = seli.where(and_(popid, popwhere, gdrwhere))
    resi = eng.execute(seli)
    query_results = resi.fetchall()
    names = []
    tmptab.drop()
    for result in query_results:
        name = result[0][0] + result[0][1:].lower()
        names.append(dict(name=name, href=result[1], mean=result[2]))
    return jsonify(dict(names=names))
