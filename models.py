from app import tmsdb
from app import app
followers = tmsdb.Table(
    'followers',
    tmsdb.Column('follower_id', tmsdb.Integer, tmsdb.ForeignKey('user.user_id')),
    tmsdb.Column('followed_id', tmsdb.Integer, tmsdb.ForeignKey('user.user_id'))
)

recommend= tmsdb.Table('recommend',tmsdb.Column('follower_id',tmsdb.Integer,tmsdb.ForeignKey('user.user_id')),
	tmsdb.Column('followed_id',tmsdb.Integer,tmsdb.ForeignKey('user.user_id')),
	tmsdb.Column('recbook_id',tmsdb.Integer,tmsdb.ForeignKey('book.book_id')))

reads=tmsdb.Table('reads',tmsdb.Column('reader_id',tmsdb.Integer,tmsdb.ForeignKey('user.user_id')),
	tmsdb.Column('book_id',tmsdb.Integer,tmsdb.ForeignKey('book.book_id')))

attempt_challenge=tmsdb.Table('attempt_challenge',tmsdb.Column('challenger_id',tmsdb.Integer,tmsdb.ForeignKey('user.user_id')),
	tmsdb.Column('challenge_id',tmsdb.Integer,tmsdb.ForeignKey('book.book_id')))


rating=tmsdb.Table('rating',tmsdb.Column('rater_id',tmsdb.Integer,tmsdb.ForeignKey('user.user_id')),
	tmsdb.Column('book_id',tmsdb.Integer,tmsdb.ForeignKey('book.book_id')),tmsdb.Column('rate',tmsdb.Integer),
	tmsdb.PrimaryKeyConstraint('rater_id', 'book_id'))

class user(tmsdb.Model):
    user_id = tmsdb.Column(tmsdb.Integer, primary_key=True)
    username = tmsdb.Column(tmsdb.String(64), index=True, unique=True, nullable=False)
    email_id = tmsdb.Column(tmsdb.String(120), index=True, unique=True, nullable=False)
    password= tmsdb.Column(tmsdb.String(32),nullable=False)
    description= tmsdb.Column(tmsdb.String(200))
    profile_pic= tmsdb.Column(tmsdb.LargeBinary)
    age=tmsdb.Column(tmsdb.DateTime)
    languages=tmsdb.Column(tmsdb.String(100),nullable=False)
    location=tmsdb.Column(tmsdb.String(50))
    genres=tmsdb.Column(tmsdb.String(150),nullable=False)
    writes=tmsdb.relationship('book',backref='author',lazy='dynamic')
    attempts=tmsdb.relationship('challenge',secondary=attempt_challenge,backref='challenger',lazy='dynamic')
    followed = tmsdb.relationship('user',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == user_id),
                               secondaryjoin=(followers.c.followed_id == user_id),
                               backref=tmsdb.backref('followers', lazy='dynamic'),
                               lazy='dynamic')
	comments=tmsdb.relationship('comment',backref='user',lazy='dynamic')
	reading=tmsdb.relationship('book',secondary=reads,backref='reader',lazy='dynamic')
	rates=tmsdb.relationship('book',secondary=rating, backref='rating',lazy='dynamic')
	recommends=tmsdb.relationship('book',secondary=recommend,backref='recommender',lazy='dynamic')


class book(tmsdb.Model):
	book_id=tmsdb.Column(tmsdb.Integer, primary_key=True)
	genre=tmsdb.Column(tmsdb.String(150),nullable=False)
	title=tmsdb.Column(tmsdb.String(50),nullable=False)
	coverpage=tmsdb.Column(tmsdb.LargeBinary)
	tags=tmsdb.Column(tmsdb.String(150))
	synopsis=tmsdb.Column(tmsdb.String(500))
	content=tmsdb.Column(tmsdb.Text)
	user_id=tmsdb.Column(tmsdb.Integer,tmsdb.ForeignKey('user.user_id'))
	story_type=tmsdb.Column(tmsdb.String(20),nullable=False)
	commented_on=tmsdb.relationship('comment',backref='book',lazy='dynamic')

class comment(tmsdb.Model):
	content=tmsdb.Column(tmsdb.String(100))
	timestamp=tmsdb.Column(tmsdb.DateTime)
	book_id=tmsdb.Column(tmsdb.Integer,tmsdb.ForeignKey('book.book_id'))
	user_id=tmsdb.Column(tmsdb.Integer,tmsdb.ForeignKey('user.user_id'))



class challenge(tmsdb.Model):
	challenge_id=tmsdb.Column(tmsdb.Integer, primary_key=True)
	timestamp=tmsdb.Column(tmsdb.DateTime)
	content=tmsdb.Column(tmsdb.String(500))
	picture_question=tmsdb.Column(tmsdb.LargeBinary)
#	user_id=tmsdb.Column(tmsdb.Integer,tmsdb.ForeignKey('user_id'))




