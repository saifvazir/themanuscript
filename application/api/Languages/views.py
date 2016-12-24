
from flask import request,jsonify,Blueprint
from application.api.Languages.functions import *
from application.models import Languages
import json
from application.api.Users.functions import InternalServerError
from application import db
from application import CreatePayload


languages = Blueprint('languages', __name__)

#api to get all the languages
@languages.route('/api/v1.0/get_languages')
def get_languages():

	try:
		AllLanguages = Languages.query.all()
	except Exception as e:
		print str(e)
		return InternalServerError()
	temp={"LangId":"", "Lang":""}
	final=[]
	for lan in AllLanguages:
		temp["LangId"] = lan.Language_id
		temp["Lang"] = lan.Name
		final.append(temp)
		temp={"LangId":"", "Lang":""}
	del temp
	return CreatePayload({"status":"True", "message":"payload contains all data"},final)


#apis for admin to add one language at a time
#auth required
@languages.route('/api/v1.0/add_language',methods=['POST'])
def add_language():
	data = json.loads(request.data)["payload"]
	name = data['language']
	temp = GenerateLanguageId(name)
	Language_id = temp["temp"]
	id = temp["count"]
	new_entry = Languages(id,Language_id,name)
	try:
		db.session.add(new_entry)
		db.session.commit()
		increaselanguagescount()
	except Exception as e:
		print str(e)
		return InternalServerError()
	return CreatePayload({"status":True, "message":"Language added successfully"},None)
