from TMS import app
from TMS.api.Users.functions import *
from flask import request,jsonify
import requests
import json
from models import Users, tmsdb, Count
from flask import session,redirect,url_for
from requests_oauthlib import OAuth2Session

oauth = OAuth()

SECRET_KEY = 'development key'
app.secret_key = SECRET_KEY


@app.route('/api/v1.0/register', methods=['POST'])
def register():
	data = json.loads(request.data)
	print data
	data = data['payload']
	if(data['is_google']==0):
		if(checkusername(data['Username'])):
			return jsonify({
				"payload":"failed",
				"message":"username already exists"
				}
				)

		# print data["Username"]
		User_id = generateuserid(data['Username'])
		Username = data['Username']
		Email_id = data['Email_id']
		pwd = encrypt_password(data['Password'])
		nw = datetime.datetime.now()
		new_entry = Users(User_id,Username,Email_id,pwd,Dateentry=nw)
		try:
			tmsdb.session.add(new_entry)
			tmsdb.session.commit()
			increaseuserscount()
		except:
			print "new user not entered some error occured"
			return jsonify({
				'payload':"failed",
				'message':"some error occured please try again"
				})

		return jsonify({
				'payload':"Success",
				'message':"User successfully created"
				})
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

@app.route('/api/v1.0/register/gcallback')
def callback():

    google = get_google_auth(state=session['oauth_state'])
    try:
        token = google.fetch_token(
            Auth.TOKEN_URI,
            client_secret=Auth.CLIENT_SECRET,
            authorization_response=request.url)
    except HTTPError:
        return 'HTTPError occurred.'
    google = get_google_auth(token=token)
    resp = google.get(Auth.USER_INFO)
    if resp.status_code == 200:
        user_data = resp.json()
        print user_data
        # email = user_data['email']
        # user = User.query.filter_by(email=email).first()
        # if user is None:
            # user = User()
            # user.email = email
        # user.name = user_data['name']
        print(token)
        # user.tokens = json.dumps(token)
        # tmsdb.session.add(user)
        # tmsdb.session.commit()
        return redirect(url_for('index'))
        return 'Could not fetch your information.'


@app.route('/')
def index():
	Users.query.all()
	return "dwaewf"

@app.route('/auth/google', methods=['POST'])
def google():
    access_token_url = 'https://accounts.google.com/o/oauth2/token'
    people_api_url = 'https://www.googleapis.com/plus/v1/people/me/openIdConnect'

    payload = dict(client_id='619494812049-rua6n3d06bjdu3vmb3e2sokfj14hv8gd.apps.googleusercontent.com',
                   redirect_uri='https://localhost:5000/api/v1.0/register/gcallback',
                   client_secret='lLk4nQN-no6Oy0uO45e39N9f',
                   scope='https://www.googleapis.com/auth/userinfo.email',
                   grant_type='client_credentials')

    # Step 1. Exchange authorization code for access token.
    r = requests.post(access_token_url, data=payload)
    token = json.loads(r.text)
    print "------------------------------------"

    print token
    print "------------------------------------"
    headers = {'Authorization': 'Bearer {0}'.format(token['access_token'])}

    # Step 2. Retrieve information about the current user.
    r = requests.get(people_api_url, headers=headers)
    profile = json.loads(r.text)

    # # Step 3. (optional) Link accounts.
    # if request.headers.get('Authorization'):
    #     user = User.query.filter_by(google=profile['sub']).first()
    #     if user:
    #         response = jsonify(message='There is already a Google account that belongs to you')
    #         response.status_code = 409
    #         return response

    #     payload = parse_token(request)

    #     user = User.query.filter_by(id=payload['sub']).first()
    #     if not user:
    #         response = jsonify(message='User not found')
    #         response.status_code = 400
    #         return response
    #     user.google = profile['sub']
    #     user.display_name = user.display_name or profile['name']
    #     db.session.commit()
    #     token = create_token(user)
    #     return jsonify(token=token)

    # Step 4. Create a new account or return an existing one.

    # user = User.query.filter_by(google=profile['sub']).first()
    # if user:
    #     token = create_token(user)
    #     return jsonify(token=token)
    # u = User(google=profile['sub'],
    #          display_name=profile['name'])
    # db.session.add(u)
    # db.session.commit()
    # token = create_token(u)
    print profile
    return "done"

@app.route('/api/v1.0/login',methods=['POST'])
def login():
    data = json.loads(request.data)
    
    try:
        user = User.query.filter_by(Username = Username).first()
    except:
        print "query failed"
        return jsonify({
            'payload':"failed",
            'message':"some error occured please try again"
            })

    if user:
        if(encrypt_password(data['Password']) == user.Password):
            session['logged_in'] = True
            return jsonify({
                'status':True,
                'message': "user authenticated successfully"
                })
        else:
            return jsonify({
                'status':False,
                'message':"Wrong username or password"
                })

    return jsonify({
        'status':False,
        'message':"Wrong username or password"
        })