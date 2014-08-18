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

@app.route("/_add_numbers")
def _blah_add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route("/db_json")
def db_json():
    keywords = request.args.get('keywords')
    # keywords = ['religious',]
    keywords = keywords.split()
    print keywords
    # with db:
    tmptab = getresults(keywords) 
    seli = sql.select([numtab.c.name, hreftab.c.href, tmptab.c.mean]).where(and_(tmptab.c.name_id==numtab.c.id, tmptab.c.name_id==hreftab.c.name_id)).order_by(tmptab.c.score.desc())
    resi = eng.execute(seli)
    query_results = resi.fetchall()
    names = []
    tmptab.drop()
    for result in query_results:
        names.append(dict(name=result[0], href=result[1], mean=result[2]))
    return jsonify(dict(names=names))

@app.route('/db')
def cities_page():
    with db:
        cur = db.cursor()
        cur.execute("select Name from city limit 15;")
        query_results = cur.fetchall()
    cities = ""
    for result in query_results:
        cities += result[0]
        cities += "<br>"
    return cities
@app.route("/db_fancy")
def cities_page_fancy():
  with db:
    cur = db.cursor()
    cur.execute("SELECT Name, CountryCode, Population FROM city ORDER BY Population LIMIT 15;")

    query_results = cur.fetchall()
  cities = []
  for result in query_results:
    cities.append(dict(name=result[0], country=result[1], population=result[2]))
  return render_template('cities.html', cities=cities) 