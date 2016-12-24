#from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from application  import db
#app.config.from_pyfile('config.cfg')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ankitesh:postgres@localhost/themanuscript'


class Count(db.Model):
	__tablename__ = 'Count'
	userscount = db.Column(db.Integer, primary_key=True)
	bookscount = db.Column(db.Integer,primary_key=True)
	languagescount = db.Column(db.Integer)


followers = db.Table('followers',
	db.Column('follower_id', db.Integer, db.ForeignKey("Users.id")),
	db.Column('followed_id', db.Integer, db.ForeignKey("Users.id"))
	)

preference = db.Table('preference',
		db.Column('uid', db.Integer, db.ForeignKey("Users.id"), nullable=False),
		db.Column('lid', db.Integer, db.ForeignKey("Languages.id"), nullable=False),
		db.PrimaryKeyConstraint('uid', 'lid')
		)
#primary language
#is_first_login
class Users(db.Model):
	__tablename__ = 'Users'
	id = db.Column(db.Integer, primary_key=True)
	User_id = db.Column(db.String(64), index=True,unique=True, nullable=False)
	Username = db.Column(db.String(64), index=True, unique=True, nullable=False)
	Email_id = db.Column(db.String(120), index=True, unique=True, nullable=False)
	Password= db.Column(db.String(40),nullable=False)
	Profile_pic= db.Column(db.String(100))
	Dob = db.Column(db.Date)
	Primary_language = db.Column(db.String(15))
	Location=db.Column(db.String(50))
	Genres=db.Column(db.String(150))
	Date_entry = db.Column(db.DateTime)
	tokens = db.Column(db.String(600))
	followed = db.relationship('Users',
								secondary=followers,
								primaryjoin= (followers.c.follower_id == id),
								secondaryjoin= (followers.c.followed_id == id),
								backref= db.backref('followers', lazy='dynamic'),
								lazy='dynamic')

	prefers = db.relationship('Languages',
								secondary=preference,
								backref=db.backref('was_preferred',lazy='dynamic')
								)

	def __init__(self,id,User_id,Username,Email_id,Password,Profile_pic=None,Age=None,Languages=None,Location=None,Genres=None, Dateentry=None):
		self.id = id
		self.User_id = User_id
		self.Username = Username
		self.Email_id = Email_id
		self.Password = Password
		self.Date_entry = Dateentry
		self.tokens = None

	def follow(self,user):
		if not self.is_following(user):
			self.followed.append(user)
			return self

	def unfollow(self,user):
		if self.is_following(user):
			self.followed.remove(user)
			return self

	def is_following(self,user):
		return self.followed.filter(followers.c.followed_id == user.id).count() > 0


class Books(db.Model):
	__tablename__ = 'Books'
	id = db.Column(db.Integer, primary_key=True)
	Book_id=db.Column(db.String(50), unique=True)
	Genre=db.Column(db.String(150),nullable=False)
	Title=db.Column(db.String(50),nullable=False)
	Coverpage=db.Column(db.String(100))
	Tags=db.Column(db.String(150))
	Content_Id=db.Column(db.String(30))
	Author_id=db.Column(db.String(30))
	Story_type=db.Column(db.String(30),nullable=False)

class Languages(db.Model):
	__tablename__ = 'Languages'
	id = db.Column(db.Integer,primary_key=True)
	Language_id = db.Column(db.String(20),unique=True)
	Name = db.Column(db.String(15))

	def __init__(self,id,Language_id,Name):
		self.id = id
		self.Language_id = Language_id
		self.Name = Name



class SecretKeys(db.Model):
	__tablename__ = "SecretKeys"
	id = db.Column(db.Integer, primary_key=True)
	Secret = db.Column(db.String(200))

	def __init__(self,id,key):
		self.id = id
		self.Secret = key

