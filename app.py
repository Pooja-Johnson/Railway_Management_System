import os
from flask import Flask, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
cd=os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(cd,'railway.sqlite3')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.../railway.sqlite3'

db = SQLAlchemy(app)
db.init_app(app)
app.app_context().push()

class Train(db.Model):
  __tablename__ = 'train'
  train_id = db.Column(db.Integer, primary_key=True)
  train_name = db.Column(db.String, unique=True, nullable=False)
  source = db.Column(db.Integer)
  dest = db.Column(db.Integer)
  
class Station(db.Model):
  __tablename__ = 'station'
  station_id = db.Column(db.Integer, primary_key=True)
  station_name = db.Column(db.String, unique=True, nullable=False)
  TAarr = db.Column(db.String, nullable=False)
  dest = db.Column(db.String)
  
class User(db.Model):
  __tablename__ = 'user'
  user_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
  user_name=db.Column(db.String)

@app.route('/')
def home():
   train = Train.query.all()
   return render_template('index.html', trains=train)


if __name__ == '__main__':
   app.run(host='0.0.0.0',debug = True,port=8080)