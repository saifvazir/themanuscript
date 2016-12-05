from TMS import app
from TMS.api.Users.functions import *
from flask import request,jsonify
import json
from models import Users, tmsdb, Count


@app.route('/api/v1.0/register', methods=['POST'])
def register():
	data = json.loads(request.data)
	print data
	data = data['payload']
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


@app.route('/')
def index():
	Users.query.all()
	return "dwaewf"