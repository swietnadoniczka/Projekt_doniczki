from flask_wtf import Form
from wtforms import TextField,StringField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, DateField, PasswordField, BooleanField
from wtforms import validators, ValidationError
from datetime import date, datetime




class UsersData(Form):
    full_name = StringField("Full_name",[validators.Required("Wprowadz to pole")])
    #car_id= TextField("Car ID",[validators.Required("Wprowadz to pole")],default="1")
    submit = SubmitField("Dodaj dane Users")


class DeviceData(Form):
    name = TextField("Name",[validators.Required("Wprowadz to pole")],default="device name")
    id= TextField("ID",[validators.Required("Wprowadz to pole")],default="5")
    user_id= TextField("User ID",[validators.Required("Wprowadz to pole")],default="5")
    submit = SubmitField("Dodaj dane Device")

class PumpData(Form):
    id= TextField("ID",[validators.Required("Wprowadz to pole")],default="3")
    water_time = TextField("Water time",[validators.Required("Wprowadz to pole")],default="50")
    dane = TextField("Dane",[validators.Required("Wprowadz to pole")],default="True")
    start_time = TextField("Start time",[validators.Required("Wprowadz to pole")],default="2023-05-14 14:15:20")
    stop_time = TextField("Stop time",[validators.Required("Wprowadz to pole")],default="2023-05-15 12:25:10")
    device_id= TextField("Device ID",[validators.Required("Wprowadz to pole")],default="5")
    submit = SubmitField("Dodaj dane Pump")
