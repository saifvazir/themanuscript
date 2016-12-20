from application.api.Users.functions import *
from flask import request,jsonify,Blueprint
import requests
import json
from application.models import Users,Count
from flask import g
from application import db
from application import auth,jwt
from flask import session,redirect,url_for
from requests_oauthlib import OAuth2Session
from boto.s3.connection import S3Connection
from boto.s3.key import Key

oauth = OAuth()
users = Blueprint('users', __name__)


def generate_auth_token(id):
    return jwt.dumps({'id':id})


@users.route('/api/v1.0/register', methods=['POST'])
def register():
	data = json.loads(request.data)["payload"]
	if(data['is_google']==0):
		if(checkusername(data['Username'])):
			return jsonify({"payload":{
                "success":False,
                "error_code":None,
                "error_message":"Username already Exists"
                }}
				)

		User_id = generateuserid(data['Username'])
		Username = data['Username']
		Email_id = data['Email_id']
		pwd = encrypt_password(data['Password'])
		nw = datetime.datetime.now()
		new_entry = Users(User_id,Username,Email_id,pwd,Dateentry=nw)
		try:
			db.session.add(new_entry)
			db.session.commit()
			increaseuserscount()
		except Exception as e:
			db.session.rollback()
            # print(str(e))
			return jsonify({"payload":{
                "success":False,
                "error_code":500,
                "error_message":"internal server error",
                "temp":str(e)
                }})


		return jsonify({"payload":{
            "success":True,
            "error_code":None,
            "error_message": None,
            "message":"User successfully registered"
            }})
# else part
	# google = get_google_auth()
	# auth_url, state = google.authorization_url(
	# Auth.AUTH_URI, access_type='offline')
	# session['oauth_state'] = state
	# # a = requests.get(auth_url)
	# # print a.text
	# # return auth_url
	# return redirect(auth_url)
	# return jsonify({
	# 		'payload':"Success",
	# 		'message':"User successfully created"
	# 		})

	# access_token = session.get('access_token')
	# if access_token is None:
	#     return redirect(url_for('login_callback'))

	# access_token = access_token[0]
	# from urllib2 import Request, urlopen, URLError

	# headers = {'Authorization': 'OAuth '+access_token}
	# req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
	#               None, headers)
	# try:
	#     res = urlopen(req)
	# except URLError, e:
	#     if e.code == 401:
	#         # Unauthorized - bad token
	#         session.pop('access_token', None)
	#         return redirect(url_for('login'))
	#     return res.read()
	# print res.read()
	# return res.read()



@users.route('/api/v1.0/login',methods=['POST'])
def login():
    
    data = json.loads(request.data)["payload"]    
    try:
        user = User.query.filter_by(Username = data['Username']).first()
    except Exception as e:
        print(str(e))
        raise e

    if user:
        if(encrypt_password(data['Password']) == user.Password):
            # session['logged_in'] = True
            token = generate_auth_token(user.User_id)
            return jsonify({
                'success':True,
                'message': "user authenticated successfully",
                'token':token
                })
        else:
            return jsonify({
                'success':False,
                'error_code':None,
                'error_message':"Wrong username or password"
                })

    return jsonify({
        "success":False,
        "error_code":None,
        'error_message':"Wrong username or password"
        })


@users.route('/protected')
@auth.login_required
def protected():
    return "this is protected"

@users.route('/set_token')
def set_token():
    token = generate_auth_token('#UOBJ110')
    return jsonify({
    'success':True,
    'message': "user authenticated successfully",
    'token':token
       })


@users.route('/set_me')
def set_me():
    token = generate_auth_token('#UOBJ14')
    return jsonify({
    'success':True,
    'message': "user authenticated successfully",
    'token':token
       })

