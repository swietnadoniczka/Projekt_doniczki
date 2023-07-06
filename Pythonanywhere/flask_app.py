
from forms import UsersData, DeviceData, PumpData
from flask import Flask, redirect, render_template, request, jsonify, abort, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc ,asc
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, pprint
from datetime import datetime, timedelta
import  os
from os.path import isfile, join
from os import listdir
import json
from io import StringIO
from werkzeug.wrappers import Response
import itertools
import random
import string

app = Flask(__name__)
app.secret_key = 'development key'

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="swietnadoniczka",
    password="alamakota", # database passowrd hidden
    hostname="swietnadoniczka.mysql.pythonanywhere-services.com",
    databasename="swietnadoniczka$doniczka2",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299 # connection timeouts
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # no warning disruptions

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Users(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(4096))



    def __init__(self, full_name):
        self.full_name = full_name



class UsersSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id' ,'full_name')
        #fields = ('id', 'full_name')


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)



@app.route("/users", methods=["GET"])
def get_all_users():
    user_many = Users.query.all()
    result = users_schema.dump(user_many)
    return jsonify(result)

@app.route("/user/<id>", methods=["GET"])
def get_all_user(id):
    user = Users.query.get(id)
    result = user_schema.dump(user)
    return jsonify(result)

@app.route("/users", methods=["POST"])
def add_user():
    full_name = request.json["full_name"]
    new_user = Users(full_name)
    db.session.add(new_user)
    db.session.commit() # PK increment
    user = Users.query.get(new_user.id)
    return user_schema.jsonify(user)


class Device(db.Model):

    __tablename__ = "device"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4096))
    user_id = db.Column(db.Integer)


    def __init__(self, name, user_id, id):
        self.name = name
        self.user_id = user_id
        self.id = id


class DeviceSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('name', 'user_id', 'id')
        #fields = ('id', 'full_name')

device_schema = DeviceSchema()
devices_schema = DeviceSchema(many=True)


@app.route("/devices", methods=["GET"])
def get_all_devices():
    device_many = Device.query.all()
    result = devices_schema.dump(device_many)
    return jsonify(result)

@app.route("/device/<id>", methods=["GET"])
def get_all_device(id):
    device = Device.query.get(id)
    result = device_schema.dump(device)
    return jsonify(result)

@app.route("/devices", methods=["POST"])
def add_device():
    name = request.json["name"]
    user_id = request.json["user_id"]
    id = request.json["id"]
    new_device = Device(name, user_id, id)
    db.session.add(new_device)
    db.session.commit() # PK increment
    device = Device.query.get(new_device.id)
    return device_schema.jsonify(device)




class Pump(db.Model):

    __tablename__ = "pump"
    id = db.Column(db.Integer, primary_key=True)
    water_time = db.Column(db.Integer)
    dane = db.Column(db.BOOLEAN)
    start_time = db.Column(db.DATETIME)
    stop_time = db.Column(db.DATETIME)
    device_id = db.Column(db.Integer)
    temperature = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    czy_wlano = db.Column(db.Integer)
    czy_wylano = db.Column(db.Integer)
    stop = db.Column(db.Integer)


    def __init__(self, id, water_time, dane, start_time, stop_time, device_id, temperature, humidity, czy_wlano, czy_wylano, stop):
        self.id = id
        self.water_time = water_time
        self.dane = dane
        self.start_time = start_time
        self.stop_time = stop_time
        self.device_id = device_id
        self.temperature = temperature
        self.humidity = humidity
        self.czy_wlano = czy_wlano
        self.czy_wylano = czy_wylano
        self.stop = stop


class PumpsSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'water_time', 'dane', 'start_time', 'stop_time', 'device_id', 'temperature', 'humidity', 'czy_wlano', 'czy_wylano', 'stop' )
        #fields = ('id', 'full_name')

pump_schema = PumpsSchema()
pumps_schema = PumpsSchema(many=True)


@app.route("/pumps", methods=["GET"])
def get_all_pumps():
    pump_many = Pump.query.all()
    result = pumps_schema.dump(pump_many)
    return jsonify(result)

@app.route("/pump/<id>", methods=["GET"])
def get_all_pump(id):
    pump = Pump.query.get(id)
    result = pump_schema.dump(pump)
    return jsonify(result)

@app.route("/pumps", methods=["POST"])
def add_pump():
    id = request.json["id"]
    water_time = request.json["water_time"]
    dane = request.json["dane"]
    start_time = request.json["start_time"]
    stop_time = request.json["stop_time"]
    device_id = request.json["device_id"]
    temperature = request.json["temperature"]
    humidity = request.json["humidity"]
    czy_wlano = request.json["czy_wlano"]
    czy_wylano = request.json["czy_wylano"]
    stop = request.json["stop"]
    new_pump = Pump(id, water_time, dane, start_time, stop_time, device_id, temperature, humidity, czy_wlano, czy_wylano, stop)
    db.session.add(new_pump)
    db.session.commit() # PK increment
    pump = Pump.query.get(new_pump.id)
    return pump_schema.jsonify(pump)


@app.route('/www/users', methods=['GET', 'POST'])
def www_get_users():
    form = UsersData()

    if request.method == 'POST':
            name = form.full_name.data
            #car_id= int(form.car_id.data)
            new_user = Users(name)
            db.session.add(new_user)
            db.session.commit()

    dev = Users.query.all()
    result = users_schema.dump(dev)
    return render_template('users.html', title = 'Users doniczki', data = result, form = form)





@app.route('/www/device', methods=['GET', 'POST'])
def www_get_device():
    form = DeviceData()



    if request.method == 'POST':
            name = form.name.data
            id= int(form.id.data)
            user_id = int(form.user_id.data)
            new_device = Device(name, id, user_id )
            db.session.add(new_device)
            db.session.commit()


    dev = Device.query.all()
    result = devices_schema.dump(dev)
    return render_template('device.html', title='Device doniczki', data= result, form=form)




@app.route('/www/pump', methods=['GET', 'POST'])
def www_get_pump():
    form = PumpData()



    if request.method == 'POST':
            id= int(form.id.data)
            water_time = int(form.water_time.data)
            dane = bool(form.dane.data)
            start_time = datetime.strptime(form.start_time.data, '%Y-%m-%d %H:%M:%S')
            stop_time = datetime.strptime(form.stop_time.data, '%Y-%m-%d %H:%M:%S')
            device_id = int(form.device_id.data)
            temperature = int(form.temperature.data)
            humidity = int(form.humidity.data)
            czy_wlano = int(form.czy_wlano.data)
            czy_wylano = int(form.czy_wylano.data)
            stop = int(form.stop.data)
            new_pump = Pump(id, water_time, dane, start_time, stop_time, device_id, temperature, humidity, czy_wlano, czy_wylano, stop )
            db.session.add(new_pump)
            db.session.commit()




    dev = Pump.query.all()
    result = pumps_schema.dump(dev)
    return render_template('pump.html', title='Pump doniczki', data= result, form=form)



@app.route('/pump/<id>', methods=['POST'])
def change_water_user(id):
    pump = Pump.query.get(id)
    if len(pump.id) == 0:
        abort(404)
    if not request.json:
        abort(400)
    pump.czy_wlano = request.json.get('czy_wlano', pump.czy_wlano)
    pump.czy_wylano = request.json.get('czy_wylano', pump.czy_wylano)
    pump.stop = request.json.get('stop', pump.stop)
    db.session.commit()
    return pump_schema.jsonify(pump_schema.dump(pump))



#@app.route('/czypodlac/<id>', methods=['GET'])
@app.route('/czypodlac2/<id>', methods=['GET'])
def czypodlac2(id):
    info = 0  # Inicjalizacja zmiennej 'info' jako 0

    # Szukanie w bazie danych pompy o danym ID
    #pump = Pump.query.get(id)
    #pump = Pump.query.filter_by(device_id=id, czy_wlano = 0)

    pumps = Pump.query.filter_by(device_id=id, czy_wlano=0)

    for pump in pumps:
        if pump.start_time < datetime.now():
            info = 1
            #break



    #if not pump:
       # abort(404)  # Zwrócenie błędu 404, jeśli pompa o podanym ID nie istnieje

    #if pump.start_time < datetime.now():
        #pump.czy_wlano = 1
        #db.session.commit()
     #   info = 1

    return str(info)  # Zwrócenie wartości 'info' jako odpowiedź
    #return datetime.now()

@app.route('/czywylac/<id>', methods=['GET'])
def czywylac(id):
    info = 0  # Inicjalizacja zmiennej 'info' jako 0

    # Szukanie w bazie danych pompy o danym ID
    pump = Pump.query.get(id)

    if not pump:
        abort(404)  # Zwrócenie błędu 404, jeśli pompa o podanym ID nie istnieje

    if pump.czy_wylano == 0 and datetime.now() > pump.stop_time:
        pump.czy_wylano = 1
        db.session.commit()
        info = 1

    if pump.czy_wylano == 1 and datetime.now() > pump.stop_time and pump.stop == 1:
        pump.czy_wylano = 0
        pump.stop = 0
        db.session.commit()
        info = 0


    return str(info)  # Zwrócenie wartości 'info' jako odpowiedź

@app.route('/czypodlac/<id>', methods=['GET'])
def czypodlac(id):
    info = 0  # Inicjalizacja zmiennej 'info' jako 0

    # Szukanie w bazie danych pompy o danym ID
    pump = Pump.query.get(id)

    if not pump:
        abort(404)  # Zwrócenie błędu 404, jeśli pompa o podanym ID nie istnieje

    if pump.czy_wlano == 0 and pump.start_time < datetime.now() < pump.stop_time and pump.stop == 0:
        pump.czy_wlano = 1
        db.session.commit()
        info = 1

    if pump.stop == 1:
        pump.czy_wlano = 0
        db.session.commit()
        info = 0


    if pump.czy_wlano == 0 and pump.stop_time < datetime.now() and pump.stop == 1:
        pump.czy_wlano = 0
        pump.stop = 0
        db.session.commit()
        info = 0


    return str(info)  # Zwrócenie wartości 'info' jako odpowiedź
