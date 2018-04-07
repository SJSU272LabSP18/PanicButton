from datetime import datetime
from flask import Flask
import googlemaps
from flask import Response
from flask import jsonify
from flask import request, render_template
from flaskext.mysql import MySQL
from flask import Markup

import plotter

# from flask.ext.mysql import MySQL

"""Cloud Foundry test"""
from flask import Flask
import os

app = Flask(__name__)
app.logger.disabled = False

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'fd3ff8a0ec0350c02a3c78c267f0b444f97561ce95a776eeae10'
app.config['MYSQL_DATABASE_DB'] = 'panicbutton'
app.config['MYSQL_DATABASE_HOST'] = 'sl-us-south-1-portal.21.dblayer.com'
app.config['MYSQL_DATABASE_PORT'] = 38220
mysql.init_app(app)

points_list = []
mymap = plotter.GoogleMapPlotter(39.8283, -98.5795, 5)

if os.getenv("VCAP_APP_PORT"):
    port = int(os.getenv("VCAP_APP_PORT"))
else:
    port = 8080


def selectAllQuery():
    try:
        db = mysql.connect()
        cursor = db.cursor()
        sql = "SELECT severity,latitude, longitude FROM panicbuttontable"
        cursor.execute(sql)
        results = cursor.fetchall()
        return results

    except Exception as e:
        app.logger.error("Error Log: %s", e)
        return "NOT OK"

@app.route("/1", methods=["GET"])
def bar():
    labels = []
    values = []
    for data in bar1Query():
        labels.append(data[0])
        values.append(data[1])
    return render_template('barchart.html', values=values, labels=labels)

@app.route("/2", methods=["GET"])
def pie():
    labels = []
    values = []
    colorpallet = []
    for data in pieQuery():
        values.append(data[0])
        labels.append(data[1])
    colors = ["#FF8000", "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA", "#ABCDEF", "#DDDDDD", "#ABCABC", "#FF4000", "#BF00FF", "#00FFFF", "#FFC0CB"]
    for i in range(0, len(values)):
        colorpallet.append(colors[i])

    return render_template('piechart.html', set=zip(values, labels, colorpallet))

@app.route("/3", methods=["GET"])
def stackedbar():
    labels = []
    data = {}
    for d in bar2Query():
        city = d[0]
        if city not in data:
            data[city] = {}

        subdict = data[city]
        s = d[1]
        if s not in subdict:
            subdict[s] = d[2]

    for l in data:
        labels.append(l)

    data1 = []
    data2 = []
    data3 = []
    data4 = []
    for key in data:
        flag = 0
        for k in data[key]:
            if k == 1:
                data1.append(data[key][k])
                flag = 1
        if flag == 0:
            data1.append(0)

    for key in data:
        flag = 0
        for k in data[key]:
            if k == 2:
                data2.append(data[key][k])
                flag = 1
        if flag == 0:
            data2.append(0)

    for key in data:
        flag = 0
        for k in data[key]:
            if k == 3:
                data3.append(data[key][k])
                flag = 1
        if flag == 0:
            data3.append(0)

    for key in data:
        flag = 0
        for k in data[key]:
            if k == 4:
                data4.append(data[key][k])
                flag = 1
        if flag == 0:
            data4.append(0)
    return render_template('stackedbarchart.html', labels=labels, data1=data1, data2=data2, data3=data3, data4=data4)

# Number of calls by city
# @app.route("/query1", methods=["GET"])
def bar1Query():
    try:
        db = mysql.connect()
        cursor = db.cursor()
        sql = "SELECT city,count(*) as totalcount FROM panicbuttontable GROUP BY city"
        cursor.execute(sql)
        results = cursor.fetchall()
        return (results)

    except Exception as e:
        app.logger.error("Error Log: %s", e)
        return "NOT OK"

# Number of calls by month
# @app.route("/query2", methods=["GET"])
def pieQuery():
    try:
        db = mysql.connect()
        cursor = db.cursor()
        sql = "SELECT count(*) as total,MONTHNAME(incidentDate) as monthname FROM panicbuttontable GROUP BY monthname"
        cursor.execute(sql)
        results = cursor.fetchall()
        return (results)

    except Exception as e:
        app.logger.error("Error Log: %s", e)
        return "NOT OK"

# Number of calls by severity and city
# @app.route("/query3", methods=["GET"])
def bar2Query():
    try:
        db = mysql.connect()
        cursor = db.cursor()
        sql = "SELECT city,severity,count(incidentID) as total FROM panicbuttontable GROUP BY city,severity"
        cursor.execute(sql)
        results = cursor.fetchall()
        return (results)

    except Exception as e:
        app.logger.error("Error Log: %s", e)
        return "NOT OK"

# @app.route("/geo", methods=["GET"])
def reverseGeocode(latitude, longitude):
    gmaps = googlemaps.Client(key='AIzaSyBy3l8CsBAn4yUrS_pUddS6iqzy0YOU6zw')
    reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))
    return (reverse_geocode_result[0]["formatted_address"])


def db(latitude, longitude, severity):
    locationdictionary = reverseGeocode(latitude, longitude)
    addArray = locationdictionary.split(',')
    address = addArray[0]
    cityName = addArray[1].strip(' ')
    stateArray = addArray[2].split(' ')
    state = stateArray[1]
    countryName = addArray[3].strip(' ')
    datetime2 = datetime.now()
    d = mysql.connect()
    cursor = d.cursor()
    query = "INSERT INTO panicbuttontable (severity,incidentDate,city,country,latitude,longitude,state,address) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    try:
        # Execute the SQL command
        cursor.execute(query,
                       (severity, datetime2.strftime('%Y-%m-%d %H:%M:%S'), cityName, countryName, latitude, longitude, state, address))
        d.commit()
        # Commit your changes in the database
        print("inserted", severity, datetime2.strftime('%Y-%m-%d %H:%M:%S'), cityName, countryName, latitude, longitude, state, address)
    except Exception as e:
        # Rollback in case there is any error
        print(e)
        d.rollback()


@app.errorhandler(400)
def bad_request(error=None, s=''):
    s = error
    message = {
        'status': 400,
        'message': 'BAD REQUEST ' + request.url,
        'reason': s
    }
    resp = jsonify(message)
    resp.status_code = 400

    return resp


@app.route("/log", methods=["GET", "PUT"])
def insert():
    lat = float(request.args.get('lat', ''))
    lng = float(request.args.get('long', ''))
    sev = int(request.args.get('sev', ''))

    if lat < -90 or lat > 90:
        return bad_request(lat)

    if lng < -180 or lng > 180:
        return bad_request(lng)

    if sev < 1 or sev > 4:
        return bad_request(sev)

    db(lat, lng, sev)

    points_list.append([lat, lng, sev])

    return Response("OK", status=200)


@app.route("/map", methods=["GET"])
def drawmap():
    for point in selectAllQuery():
        lat = point[1]
        lng = point[2]
        sev = point[0]
        path = [[lat], [lng]]

        if (sev is 1):
            mymap.heatmap(path[0], path[1], threshold=10, radius=30, dissipating=True,
                          gradient=[(255, 255, 0, 0), (255, 255, 0, 10), (255, 255, 0, 10), (255, 255, 0, 10), (255, 255, 0, 10),
                                    (255, 255, 0, 10), (255, 255, 0, 10)])
        elif (sev is 2):
            mymap.heatmap(path[0], path[1], threshold=10, radius=30, dissipating=True,
                          gradient=[(255, 140, 0, 0), (255, 140, 0, 10), (255, 140, 0, 10), (255, 140, 0, 10),
                                    (255, 140, 0, 10), (255, 140, 0, 10), (255, 140, 0, 10)])

        elif (sev is 3):
            mymap.heatmap(path[0], path[1], threshold=10, radius=30, dissipating=True,
                          gradient=[(255, 0, 0, 0), (255, 0, 0, 10), (255, 0, 0, 10), (255, 0, 0, 10),
                                    (255, 0, 0, 10), (255, 0, 0, 10), (255, 0, 0, 10)])
        else:
            mymap.heatmap(path[0], path[1], threshold=10, radius=30, dissipating=True,
                          gradient=[(128, 0, 0, 0), (128, 0, 0, 10), (128, 0, 0, 10), (128, 0, 0, 10),
                                    (128, 0, 0, 10), (128, 0, 0, 10), (128, 0, 0, 10)])

        mymap.setter_latlong(lat, lng)

    return mymap.draw()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
