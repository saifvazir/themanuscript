from app import db
from app import app
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.user_id'))
)

recommend= db.Table('recommend',db.Column('follower_id',db.Integer,db.ForeignKey('user.user_id')),
	db.Column('followed_id',db.Integer,db.ForeignKey('user.user_id')),
	db.Column('recbook_id',db.Integer,db.ForeignKey('book.book_id')))

reads=db.Table('reads',db.Column('reader_id',db.Integer,db.ForeignKey('user.user_id')),
	db.Column('book_id',db.Integer,db.ForeignKey('book.book_id')))

attempt_challenge=db.Table('attempt_challenge',db.Column('challenger_id',db.Integer,db.ForeignKey('user.user_id')),
	db.Column('challenge_id',db.Integer,db.ForeignKey('book.book_id')))


rating=db.Table('rating',db.Column('rater_id',db.Integer,db.ForeignKey('user.user_id')),
	db.Column('book_id',db.Integer,db.ForeignKey('book.book_id')),db.Column('rate',db.Integer),
	db.PrimaryKeyConstraint('rater_id', 'book_id'))

class user(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email_id = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password= db.Column(db.String(32),nullable=False)
    description= db.Column(db.String(200))
    profile_pic= db.Column(db.LargeBinary)
    age=db.Column(db.DateTime)
    languages=db.Column(db.String(100),nullable=False)
    location=db.Column(db.String(50))
    genres=db.Column(db.String(150),nullable=False)
    writes=db.relationship('book',backref='author',lazy='dynamic')
    attempts=db.relationship('challenge',secondary=attempt_challenge,backref='challenger',lazy='dynamic')
    followed = db.relationship('user',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == user_id),
                               secondaryjoin=(followers.c.followed_id == user_id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')
	comments=db.relationship('comment',backref='user',lazy='dynamic')
	reading=db.relationship('book',secondary=reads,backref='reader',lazy='dynamic')
	rates=db.relationship('book',secondary=rating, backref='rating',lazy='dynamic')
	recommends=db.relationship('book',secondary=recommend,backref='recommender',lazy='dynamic')


class book(db.Model):
	book_id=db.Column(db.Integer, primary_key=True)
	genre=db.Column(db.String(150),nullable=False)
	title=db.Column(db.String(50),nullable=False)
	coverpage=db.Column(db.LargeBinary)
	tags=db.Column(db.String(150))
	synopsis=db.Column(db.String(500))
	content=db.Column(db.Text)
	user_id=db.Column(db.Integer,db.ForeignKey('user.user_id'))
	story_type=db.Column(db.String(20),nullable=False)
	commented_on=db.relationship('comment',backref='book',lazy='dynamic')

class comment(db.Model):
	content=db.Column(db.String(100))
	timestamp=db.Column(db.DateTime)
	book_id=db.Column(db.Integer,db.ForeignKey('book.book_id'))
	user_id=db.Column(db.Integer,db.ForeignKey('user.user_id'))



class challenge(db.Model):
	challenge_id=db.Column(db.Integer, primary_key=True)
	timestamp=db.Column(db.DateTime)
	content=db.Column(db.String(500))
	picture_question=db.Column(db.LargeBinary)
#	user_id=db.Column(db.Integer,db.ForeignKey('user_id'))




