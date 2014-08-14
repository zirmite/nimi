from flask import Flask,render_template,jsonify,request
from app import app
import pymysql as psql

db = psql.connect(user="root", passwd="", host="localhost", db="ny_hospitals", charset='utf8')

@app.route('/')
@app.route('/index')

# def index():
#     return render_template("index.html",
#         title = 'Home', user = { 'nickname': 'Courtney' },
#         )

# @app.route('/db')
# def cities_page():
#     with db: 
#         cur = db.cursor()
#         cur.execute("SELECT Name FROM city LIMIT 15;")
#         query_results = cur.fetchall()
#     cities = ""
#     for result in query_results:
#         cities += result[0]
#         cities += "<br>"
#     return cities

# @app.route("/db_fancy")
# def cities_page_fancy():
#     with db:
#         cur = db.cursor()
#         cur.execute("SELECT Name, CountryCode, \
#             Population FROM city ORDER BY Population LIMIT 15;")

#         query_results = cur.fetchall()
#     cities = []
#     for result in query_results:
#         cities.append(dict(name=result[0], country=result[1], population=result[2]))
#     return render_template('cities.html', cities=cities) 

@app.route("/jquery")
def index_jquery():
    return render_template('index.html')

#@app.route("/db_json")
#def games_json():
#    with db:
#        cur = db.cursor()
#        cur.execute("SELECT GAME_NAME, URL, IMAGE  FROM Basics LIMIT 15;")
#        query_results = cur.fetchall()
#    games = []
#    for result in query_results:
#        games.append(dict(game=result[0], url=result[1], image=result[2]))
#    return jsonify(dict(games=games))

# @app.before_request
# def before_request():
#     if request.path != '/':
#         if request.headers['content-type'].find('application/json'):
#             return 'Unsupported Media Type', 415
 
# # @app.route('/')
# # def index():
# #     return render_template('index1.html')

@app.route('/echo/', methods=['GET'])
def echo():
    ret_data = {'diagValue': request.args.get('diagValue'),
                'ageValue':  request.args.get('ageValue')}
    age = int(ret_data['ageValue'])

    age_group = '0 to 17'
    if   age >= 18 and age < 30:
        age_group = '18 to 29'
    elif age >= 30 and age < 49:
        age_group = '30 to 49'
    elif age >= 49 and age < 69:
        age_group = '50 to 69'
    else:
        age_group = '70 or Older'

    print age
    print age_group
   

    with db:
        cur = db.cursor()
        sql = "SELECT facility_name, AVG(total_charges)             \
               FROM hospital_discharge                              \
               WHERE apr_mdc_descr = '" + ret_data['diagValue'] + "'\
               AND                                                  \
               age_group     = '" + age_group +                   "'\
               GROUP BY facility_name                               \
               ORDER BY AVG(total_charges)"
        cur.execute(sql)
        query_results = cur.fetchall()

    hospital = []
    for i, result in enumerate(query_results):
        if i > 10:
            break
        hospital.append(dict(name=result[0], avr_total_charges=int(float(result[1]))))

    return jsonify(dict(hospital=hospital))
