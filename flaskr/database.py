from flask import Flask
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

app = Flask(
    __name__,  # the name of the current file
    static_url_path="/python",  # access static file via /python/filename
    static_folder="static",  # the folder where static files at
    template_folder="templates",  # the folder where templates files at
)
# db config
app.app_context().push()
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql://root:password@localhost/Youbike"  # mod by your self
db = SQLAlchemy(app)

Session = sessionmaker(bind=db.engine)


class User(db.Model):
    CardID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20), nullable=False)
    Rent_bike_serial = db.Column(db.Integer, nullable=True)


class Bike(db.Model):
    Serial_num = db.Column(db.Integer, primary_key=True)
    Factory = db.Column(db.String(60), nullable=False)
    Is_broken = db.Column(db.Boolean, nullable=False)
    Is_using = db.Column(db.Boolean, nullable=False)
    Maintenance_record = db.Column(db.Integer, nullable=False)
    Maintenance_Employee = db.Column(db.Integer, nullable=False)
    Park_loc = db.Column(db.String(20), nullable=False)


class Location(db.Model):
    Name = db.Column(db.String(20), primary_key=True)
    Street = db.Column(db.String(30), nullable=False)
    District = db.Column(db.String(30), nullable=False)
    City = db.Column(db.String(30), nullable=False)
    Control_Employee = db.Column(db.Integer, nullable=False)


class Employee(db.Model):
    Ssn = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20), nullable=False)
    Sex = db.Column(db.String(10), nullable=False)


class Ensurance(db.Model):
    CardID = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.Integer, primary_key=True)
    Amount = db.Column(db.Integer, nullable=False)


class Rent_history(db.Model):
    Start_loc = db.Column(db.String(30), primary_key=True)
    Stop_loc = db.Column(db.String(30), primary_key=True)
    Bike_serial = db.Column(db.Integer, primary_key=True)
    User_cardID = db.Column(db.Integer, primary_key=True)
    History_serial = db.Column(db.Integer, primary_key=True)
    Cost = db.Column(db.Integer, nullable=False)
    Time = db.Column(db.Integer, nullable=False)
