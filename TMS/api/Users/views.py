from TMS import app
from flask import request
import json
from models import Users, tmsdb, Count
import hashlib
import datetime

def checkusername(Username):
	
	try:
		result = Users.query.filter_by(Username=Username).first()
	except:
		print "query not successfull"

	if(result):
		return True
	else:
		return False
	

def encrypt_password(password):
	return hashlib.md5(password).hexdigest()

def increasecount(tablename):
	result = Count.query.all()[0]
	result.tablename += result.tablename
	try:
		tmsdb.session.commit()
	except:
		print "error occured"


def generateuserid(username):
	temp = '#UOBJ'
	temp += str(len(username))[0]
	try:
		noofusers = Count.query.with_entities(Count.userscount)
	except:
		print "query not successfull"
	temp += str(noofusers[0][0])
	return temp

@app.route('/register', methods=['POST'])
def register():
	data = json.loads(request.data)
	print data
	if(checkusername(data['Username'])):
		return jsonify({
			'payload':"failed"
			'message':"username already exists"
			})

	User_id = generateuserid(data['Username'])
	Username = data['Username']
	Email_id = data['Email_id']
	pwd = encrypt_password(data['Password'])
	nw = datetime.datetime.now()
	new_entry = Users(User_id,Username,Email_id,pwd,Dateentry=nw)
	try:
		tmsdb.session.add(new_entry)
		tmsdb.session.commit()
		increasecount(userscount)
	except:
		print "new user not entered some error occured"
		return jsonify({
			'payload':"failed"
			'message':"some error occured please try again"
			})

	return jsonify({
			'payload':"Success"
			'message':"User successfully created"
			})


@app.route('/')
def index():
	Users.query.all()
	return "dwaewf"