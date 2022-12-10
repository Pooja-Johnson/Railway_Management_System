import os
from flask import Flask, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
cd = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(cd, 'railway.sqlite3')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.../railway.sqlite3'

db = SQLAlchemy(app)
db.init_app(app)
app.app_context().push()


class Train(db.Model):
    train_id = db.Column(db.Integer, primary_key=True)
    train_name = db.Column(db.String, unique=True, nullable=False)
    source = db.Column(db.Integer)  # foreign key
    dest = db.Column(db.Integer)  # foreign key
    seats_no = db.Column(db.Integer)


class Seats(db.Model):
    seat_no = db.Column(db.Integer, primary_key=True)
    availTA = db.Column(db.Integer)  # boolean
    availTB = db.Column(db.Integer)  # boolean
    availTC = db.Column(db.Integer)  # boolean


class Station(db.Model):
    station_id = db.Column(db.Integer, primary_key=True)
    station_name = db.Column(db.String, unique=True, nullable=False)
    TAarr = db.Column(db.Integer)  # boolean
    TBarr = db.Column(db.Integer)  # boolean
    TCarr = db.Column(db.Integer)  # boolean


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    gender = db.Column(db.String)
    age = db.Column(db.Integer)
    mob_no = db.Column(db.Integer)


class Ticket(db.Model):
    ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)  # foreign key
    name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String)
    b_point = db.Column(db.String)
    d_point = db.Column(db.String)
    seat_no = db.Column(db.Integer)  # foreign key
    fare = db.Column(db.Integer)


class FoodOrder(db.Model):
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)  # foreign key
    item = db.Column(db.String)
    category = db.Column(db.String)
    qty = db.Column(db.String)
    price = db.Column(db.Integer)
    train_id = db.Column(db.Integer)  # foreign key
    station_name = db.Column(db.String)  # foreign key


# db.create_all()          need to call initially only once to create tables

@app.route('/')
def home():
    train = Train.query.all()
    return render_template('index.html', trains=train)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
