@users.route('/auth/google', methods=['POST'])
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


# @users.route('/upload_images')
# def upload_images():
#     conn = S3Connection("AKIAIDO2ENODGWL4CUNA", "ofduq4s9R/yMjOq0rODITcoPjMfr2EXM4kC9zuCr")
#     bucket = conn.get_bucket('tmsuseravatars')
#     # access_key = "AKIAIDO2ENODGWL4CUNA"
#     # SECRET_KEY = "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"
#     k = Key(bucket)
#     data_file = open('/home/ankitesh/TMS/Tms/application/api/Users/abcd.jpg',"r")
#     k.key = 'abcd.jpg'
#     k.set_contents_from_string(data_file.read())
#     return "done"


@users.route('/api/v1.0/register/gcallback')
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
        # db.session.add(user)
        # db.session.commit()
        return redirect(url_for('index'))
        return 'Could not fetch your information.'
