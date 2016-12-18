
import hashlib
import datetime
from application.models import Users,Count
from application import db
#from TMS import app
from flask_oauth import OAuth
from requests_oauthlib import OAuth2Session

#app.config.from_pyfile('config.cfg')

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
		print(str(e))
		raise e

	if(result):
		return True
	else:
		return False
	

def encrypt_password(password):
	return hashlib.md5(password).hexdigest()

def increaseuserscount():
	result = Count.query.all()[0]
	result.userscount += 1
	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(str(e))
		raise e


def generateuserid(username):
	temp = '#UOBJ'
	temp += str(len(username))[0]
	noofusers = ""
	try:
		noofusers = Count.query.with_entities(Count.userscount)
	except Exception as e:
		print str(e)
		raise e
	temp += str(noofusers[0][0]+1)
	return temp


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


