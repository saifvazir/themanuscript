
import hashlib
import datetime
from models import Users, tmsdb, Count



def checkusername(Username):
	
	result=""
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

def increaseuserscount():
	result = Count.query.all()[0]
	result.userscount += 1
	try:
		tmsdb.session.commit()
	except:
		print "error occured"


def generateuserid(username):
	temp = '#UOBJ'
	temp += str(len(username))[0]
	noofusers = ""
	try:
		noofusers = Count.query.with_entities(Count.userscount)
		print "awegrtyui"
	except:
		print "query not successfull"
	temp += str(noofusers[0][0]+1)
	return temp
