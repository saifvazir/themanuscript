from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.cfg')


tmsdb = SQLAlchemy(app)

class user(db.Model):
    User_id = db.Column(ddb.String(64), primary_key=True)
    Username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    Email_id = db.Column(db.String(120), index=True, unique=True, nullable=False)
    Password= db.Column(db.String(32),nullable=False)
    Profile_pic= db.Column(db.LargeBinary)
    Age=db.Column(db.DateTime)
    Languages=db.Column(db.String(100),nullable=False)
    Location=db.Column(db.String(50))
    Genres=db.Column(db.String(150),nullable=False)
    Writes=db.relationship('book',backref='author',lazy='dynamic')
    Attempts=db.relationship('challenge',secondary=attempt_challenge,backref='challenger',lazy='dynamic')
    Followed = db.relationship('user',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == user_id),
                               secondaryjoin=(followers.c.followed_id == user_id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')
	Reading=db.relationship('book',secondary=reads,backref='reader',lazy='dynamic')


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

