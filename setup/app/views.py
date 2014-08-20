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
    print request.form
    keywords = keywords.split()
    # print male, female
    print request.method
    if male=='true':
        male = 1
    else:
        male = 0
    if female=='true':
        female = 1
    else:
        female = 0
    # with db:
    tmptab = getresults(keywords) 
    seli = sql.select([numtab.c.name, hreftab.c.href, tmptab.c.mean]).where(and_(tmptab.c.name_id==numtab.c.id, tmptab.c.name_id==hreftab.c.name_id, numtab.c.M==male, numtab.c.F==female)).order_by(tmptab.c.score.desc())
    resi = eng.execute(seli)
    query_results = resi.fetchall()
    names = []
    tmptab.drop()
    for result in query_results:
        name = result[0][0] + result[0][1:].lower()
        names.append(dict(name=name, href=result[1], mean=result[2]))
    return jsonify(dict(names=names))
