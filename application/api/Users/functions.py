
import hashlib
import datetime
from application.models import Users,Count,SecretKeys
from flask import jsonify
from application import db
import random
from application import application
import string
#from TMS import app
from flask_oauth import OAuth
from requests_oauthlib import OAuth2Session

#app.config.from_pyfile('config.cfg')
DEFAULT_PROFILE_PIC = 'aws_s3_url'

class Auth:
	CLIENT_ID = ('619494812049-rua6n3d06bjdu3vmb3e2sokfj14hv8gd'
				 '.apps.googleusercontent.com')
	CLIENT_SECRET = 'lLk4nQN-no6Oy0uO45e39N9f'
	REDIRECT_URI = 'https://localhost:5000/api/v1.0/register/gcallback'
	AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
	TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
	USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
	SCOPE = ['profile', 'email']


def checkusername(Username):
	
	result=""
	try:
		result = Users.query.filter_by(Username=Username).first()
	except Exception as e:
		db.session.rollback()
		application.logger.debug(str(e))
		raise e

	if(result):
		return True
	else:
		return False


def checkemail(email):
	result = ""
	try:
		result = Users.query.filter_by(Email_id=email).first()
	except Exception as e:
		db.session.rollback()
		application.logger.debug(str(e))
		raise e

	if (result):
		return True
	else:
		return False


def encrypt(text):
	return hashlib.md5(text).hexdigest()

def increaseuserscount():
	result = Count.query.all()[0]
	result.userscount += 1
	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		application.logger.debug(str(e))
		raise e


def generateuserid(username):
	temp = '#UOBJ'
	temp += str(len(username))[0]
	noofusers = ""
	try:
		noofusers = Count.query.with_entities(Count.userscount).first()
	except Exception as e:
		application.logger.debug(str(e))
		db.session.rollback()
		raise e
	a = noofusers[0]
	temp += str(noofusers[0]+1)
	return {"count":a+1, "temp":temp}


def get_google_auth(state=None, token=None):
	if token:
		return OAuth2Session(Auth.CLIENT_ID, token=token)
	if state:
		return OAuth2Session(
			Auth.CLIENT_ID,
			state=state,
			redirect_uri=Auth.REDIRECT_URI)
	oauth = OAuth2Session(
		Auth.CLIENT_ID,
		redirect_uri=Auth.REDIRECT_URI,
		scope=Auth.SCOPE)
	return oauth

def generate_keys():
	text = string.digits+string.letters

	for i in range(1,11,1):
		key = "".join([random.choice(text) for j in range(30)])
		new_key = SecretKeys(i, key)
		print new_key
		try:
			db.session.add(new_key)
			db.session.commit()
		except Exception as e:
			application.logger.debug(str(e))
			db.session.rollback()
			raise e


def InternalServerError():
	return jsonify({"success":{"status":False}, "payload":None, "error":{"code":500, "message":"Internal server error"}})

#Function to convert user object to data that is required for the followers page
def UsersObjectToFollowersData(UsersObj):
	final = []
	temp = {"user_id":"", "avatar":"", "username":"", "location":""}
	for userobj in UsersObj:
		temp["user_id"] = userobj.User_id
		temp["username"] = userobj.Username
		if userobj.Profile_pic:
			temp["avatar"] = userobj.Profile_pic
		else:
			temp["avatar"] = DEFAULT_PROFILE_PIC
		if userobj.Location:
			temp["location"] = userobj.Location
		final.append(temp)
		temp = {"user_id": "", "avatar": "", "username": "", "location": ""}
	del temp
	return final
