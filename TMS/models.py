from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.cfg')


tmsdb = SQLAlchemy(app)

class Books(tmsdb.Model):
	__tablename__ = 'Books'
	Book_id=tmsdb.Column(tmsdb.String(50), primary_key=True)
	Genre=tmsdb.Column(tmsdb.String(150),nullable=False)
	Title=tmsdb.Column(tmsdb.String(50),nullable=False)
	Coverpage=tmsdb.Column(tmsdb.LargeBinary)
	Tags=tmsdb.Column(tmsdb.String(150))
	Content_Id=tmsdb.Column(tmsdb.String(50),tmsdb.ForeignKey('Content_id'))
	Author_id=tmsdb.Column(tmsdb.String(50),tmsdb.ForeignKey('Author_id'))
	Story_type=tmsdb.Column(tmsdb.String(20),nullable=False)

