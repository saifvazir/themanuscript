#from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from application  import db
#app.config.from_pyfile('config.cfg')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ankitesh:postgres@localhost/themanuscript'


class Count(db.Model):
    __tablename__ = 'Count'
    userscount = db.Column(db.Integer, primary_key=True)
    bookscount = db.Column(db.Integer, primary_key=True)

class Users(db.Model):
    __tablename__ = 'Users'
    User_id = db.Column(db.String(64), primary_key=True)
    Username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    Email_id = db.Column(db.String(120), index=True, unique=True, nullable=False)
    Password= db.Column(db.String(40),nullable=False)
    Profile_pic= db.Column(db.String(100))
    Age=db.Column(db.DateTime)
    Languages=db.Column(db.String(100))
    Location=db.Column(db.String(50))
    Genres=db.Column(db.String(150))
    Date_entry = db.Column(db.DateTime)
    tokens = db.Column(db.String(1000))

    def __init__(self,User_id,Username,Email_id,Password,Profile_pic=None,Age=None,Languages=None,Location=None,Genres=None, Dateentry=None):
    	self.User_id = User_id
    	self.Username = Username
    	self.Email_id = Email_id
    	self.Password = Password
    	self.Date_entry = Dateentry
        self.tokens = None



class Books(db.Model):
	__tablename__ = 'Books'
	Book_id=db.Column(db.String(50), primary_key=True)
	Genre=db.Column(db.String(150),nullable=False)
	Title=db.Column(db.String(50),nullable=False)
	Coverpage=db.Column(db.String(100))
	Tags=db.Column(db.String(150))
	Content_Id=db.Column(db.String(30))
	Author_id=db.Column(db.String(30))
	Story_type=db.Column(db.String(30),nullable=False)


class SecretKeys(db.Model):
    __tablename__ = "SecretKeys"
    id = db.Column(db.Integer, primary_key=True)
    Secret = db.Column(db.String(200))

    def __init__(self,id,key):
        self.id = id
        self.Secret = key
