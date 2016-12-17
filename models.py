from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.cfg')


tmsdb = SQLAlchemy(app)

class Count(tmsdb.Model):
    __tablename__ = 'Count'
    userscount = tmsdb.Column(tmsdb.String(64), primary_key=True)
    bookscount = tmsdb.Column(tmsdb.String(64), primary_key=True)

class Users(tmsdb.Model):
    __tablename__ = 'Users'
    User_id = tmsdb.Column(tmsdb.String(64), primary_key=True)
    Username = tmsdb.Column(tmsdb.String(64), index=True, unique=True, nullable=False)
    Email_id = tmsdb.Column(tmsdb.String(120), index=True, unique=True, nullable=False)
    Password= tmsdb.Column(tmsdb.String(32),nullable=False)
    Profile_pic= tmsdb.Column(tmsdb.LargeBinary)
    Age=tmsdb.Column(tmsdb.DateTime)
    Languages=tmsdb.Column(tmsdb.String(100),nullable=False)
    Location=tmsdb.Column(tmsdb.String(50))
    Genres=tmsdb.Column(tmsdb.String(150),nullable=False)
    Dateentry = tmsdb.Column(tmsdb.DateTime)

    def __init__(self,User_id,Username,Email_id,Password,Profile_pic=None,Age=None,Languages=None,Location=None,Genres=None, Dateentry=None):
    	self.User_id = User_id
    	self.Username = Username
    	self.Email_id = Email_id
    	self.Password = Password
    	self.Dateentry = Dateentry


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

