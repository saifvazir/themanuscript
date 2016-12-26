
from application.api.Users.functions import *
from flask import request,jsonify,make_response
import json
from application.models import Users,SecretKeys
from application import db
import random
from application import application
from application import CreatePayload
from flask import session,redirect,url_for
from requests_oauthlib import OAuth2Session
from boto.s3.connection import S3Connection
from boto.s3.key import Key

from application.api.Users import users
from application import auth,jwt
oauth = OAuth()
FOLLOWERS_PER_PAGE = 22
# DEFAULT_PROFILE_PIC = 'aws_s3_url'

def generate_auth_token(id):
	id = random.randint(1, 10)
	application.config['SECRET_KEY'] = SecretKeys.query.filter_by(id=id)
	return jwt.dumps({'id':id})

@users.route('/api/v1.0/register', methods=['POST'])
def register():
	data = json.loads(request.data)["payload"]
	if(data['is_google']==0):
		if(checkusername(data['Username'])):
			return make_response(CreatePayload({"status":False}, None, {"code":400, "message":"Username already exists"}),400)
		if(checkemail(data["Email_id"])):
			return make_response(CreatePayload({"status":False}, None, {"code":400, "message":"Email already registered"}),400)

		temp = generateuserid(data['Username'])
		User_id = temp["temp"]
		id = temp["count"]
		Username = data['Username']
		Email_id = data['Email_id']
		#vaidate email id
		pwd = encrypt(data['Password'])
		nw = datetime.datetime.now()
		new_entry = Users(id = id, User_id=encrypt(User_id),Username=Username,Email_id=Email_id,Password=pwd,Dateentry=nw)
		try:
			db.session.add(new_entry)
			db.session.commit()
			increaseuserscount()
		except Exception as e:
			db.session.rollback()
			application.logger.debug(str(e))
			return InternalServerError()

		return make_response(CreatePayload({"status":True,"message":"user created successfully"},None),200)
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

#end point for validating username and email id
@users.route('/api/v1.0/validate')
def validate():
	try:
		username = request.args.get('username')
		#check username
		if(checkusername(username)):
			return make_response(CreatePayload({"status":False}, None, {"code":400, "message":"Username already exists"}),400)
		else:
			return make_response(CreatePayload({"status":True,"message":"username can be taken"}, None),200)
	except Exception as e:
		try:
			email = request.args.get('email')
			#check email
			if(checkemail(email)):
				return make_response(CreatePayload({"status":False}, None, {"code":400, "message":"already registered with this mail"}),400)

			else:
				return make_response(CreatePayload({"status": True, "message":"email allowed"}, None), 200)
		except Exception as e1:
			application.logger.debug(str(e1))
	return make_response(CreatePayload({"status":False}, None, {"code":400, "message":"bad request"}),400)


@users.route('/api/v1.0/login',methods=['POST'])
def login():
	
	data = json.loads(request.data)["payload"]    
	try:
		user = Users.query.filter_by(Username = data['Username']).first()
	except Exception as e:
		application.logger.debug(str(e))
		return make_response(InternalServerError(),500)
	if user:
		if(encrypt(data['Password']) == user.Password):
			# session['logged_in'] = True
			token = generate_auth_token(user.User_id)
			token += '.'+user.User_id
			curr_datetime = datetime.datetime.now()
			curr_datetime += datetime.timedelta(days=4)
			application.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'

			#no previos tokens present
			if not user.tokens:
				token_data = [{"token":token, "expiration":str(curr_datetime)}]  #1st login

			#previos tokens are present
			else:
				token_data = json.loads(user.tokens)["payload"]   # previous logged in session is active
				if(len(token_data)==2):                           #max two sessions allowed
					token_data.pop(0)

				token_data.append({"token":token, "expiration":str(curr_datetime)})
			user.tokens = json.dumps({"payload":token_data})
			try:
				db.session.commit()
			except Exception as e:
				db.session.rollback()
				application.logger.debug(str(e))
				return make_response(InternalServerError(),500)

			
			return make_response(CreatePayload({"status":True, "message":"User authenticates successfully"}, {
				"token": token,
				"user_id": user.User_id
			}),200)


		#wrong password
		else:
			return make_response(CreatePayload({"status":False}, None, {"code":401, "message":"wrong username or password"}),401)

	# no such user exists
	return make_response(CreatePayload({"status":False}, None, {"code":401, "message":"wrong username or password"}),401)


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
############################################################################################################################
###########################################apis related to following and followers module###################################
############################################################################################################################

#api to get 22 followers one at a time
@auth.login_required
@users.route('/api/v1.0/get_followers', methods=['POST'])
def get_followers():
	data = json.loads(request.data)["payload"]
	UserId = data['user']
	PageNo = data['page']
	try:
		user = Users.query.filter_by(User_id=UserId).first()
	except Exception as e:
		application.logger.debug(str(e))
		return make_response(InternalServerError(),500)
	if user:
		FollowersQueryObj = user.followers.paginate(PageNo,FOLLOWERS_PER_PAGE,False)
		#if no followers
		if not FollowersQueryObj.items:
			return make_response(CreatePayload({"status":True,"message":"No followers"},{"followers":None, "next_page":False}),200)
		#atleast one follower
		else:
			followers = UsersObjectToFollowersData(FollowersQueryObj.items)
			if FollowersQueryObj.has_next:
				next_page = PageNo+1
			else:
				next_page = False

			return make_response(CreatePayload({"status":True, "message":"Followers in payload"},{"followers":followers,"next_page":next_page}),200)

	return make_response(CreatePayload({"status":False},None,{"code":401, "message" :"no such user"}),401)

#api to get 22 users that is being followed by the route calling user
@users.route('/api/v1.0/get_followed', methods=['POST'])
def get_followed():
	data = json.loads(request.data)["payload"]
	UserId = data['user']
	PageNo = data['page']
	try:
		user = Users.query.filter_by(User_id=UserId).first()
	except Exception as e:
		application.logger.debug(str(e))
		return make_response(InternalServerError(),500)
	if user:
		FollowedQueryObj = user.followed.paginate(PageNo, FOLLOWERS_PER_PAGE, False)
		#if the caller is not following anyone
		if not FollowedQueryObj.items:
			return make_response(CreatePayload({"status":True,"message":"follows none"},{"followed":None, "next_page":False}),200)
		#the caller is following atleast one other user
		else:
			followed = UsersObjectToFollowersData(FollowedQueryObj.items)
			if FollowedQueryObj.has_next:
				next_page = PageNo+1
			else:
				next_page = False
			return make_response(CreatePayload({"status":True, "message":"Followed users in payload"},{"followed":followed,"next_page":next_page}),200)
	return make_response(CreatePayload({"status":False},None,{"code":401, "message" :"no such user"}),401)

################################################folllow and unfollow link###########################################

@users.route('/api/v1.0/follow',methods=['POST'])
def follow():

	data = json.loads(request.data)["payload"]
	FollowerId = data['follower']
	FollowedId = data['followed']
	try:
		FollowerUser = Users.query.filter_by(User_id=FollowerId).first()
		FollowedUser = Users.query.filter_by(User_id=FollowedId).first()
	except Exception as e:
		application.logger.debug(str(e))
		return make_response(InternalServerError(),500)
	if FollowerUser and FollowedUser:
		FollowerUser = FollowerUser.follow(FollowedUser)
		try:
			db.session.add(FollowerUser)
			db.session.commit()
		except Exception as e:
			application.logger.debug(str(e))
			db.session.rollback()
			return make_response(InternalServerError(),500)

		return make_response(CreatePayload({"status":True, "message":"followed successfully"},None),201)
	return make_response(CreatePayload({"status":False}, None, {"code":401,"message":"no such user exists"} ),400)
#unfollow api
@users.route('/api/v1.0/unfollow', methods=['POST'])
def unfollow():
	data = json.loads(request.data)["payload"]
	FollowerId = data['follower']
	FollowedId = data['followed']
	try:
		FollowerUser = Users.query.filter_by(User_id=FollowerId).first()
		FollowedUser = Users.query.filter_by(User_id=FollowedId).first()
	except Exception as e:
		application.logger.debug(str(e))
		return make_response(InternalServerError(),500)
	if FollowerUser and FollowedUser:
		FollowerUser = FollowerUser.unfollow(FollowedUser)
		try:
			db.session.add(FollowerUser)
			db.session.commit()
		except Exception as e:
			application.logger.debug(str(e))
			db.session.rollback()
			return make_response(InternalServerError(),500)

		return make_response(CreatePayload({"status":True, "message":"unfollowed successfully"},None),201)
	return make_response(CreatePayload({"status":False}, None, {"code":401,"message":"no such user exists"} ),401)
