
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

tmsdb = SQLAlchemy(app)


class Example(tmsdb.Model):
	__tablename__ = 'Example'
	id = db.Column('id', db.Integer, primary_key=True)
	data = db.Column('data', db.Unicode)