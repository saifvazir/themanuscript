from TMS import app
from flask import request
import json
from models import Users, tmsdb, Count
import hashlib
import datetime

def checkusername(username):
	Users.query.filter_by('Username'=Username).first()

def encrypt_password(password):
	return hashlib.md5(password).hexdigest()

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
	return jsonify({
		
		})


@app.route('/')
def index():
	Users.query.all()
	return "dwaewf"