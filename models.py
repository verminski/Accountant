from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, nullable=False)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operation = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

def add_event(operation, message):
    new_event = History(operation=operation, message=message, timestamp=datetime.datetime.now())

    return new_event