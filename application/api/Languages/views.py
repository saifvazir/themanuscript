
from flask import request,make_response
from application.api.Languages.functions import *
from application.models import Languages
import json
from application.api.Users.functions import InternalServerError
from application import db
from application import CreatePayload
from application import application


from application.api.Languages import languages
#api to get all the languages
@languages.route('/api/v1.0/get_languages')
def get_languages():

	try:
		AllLanguages = Languages.query.all()
	except Exception as e:
		application.logger.debug(str(e))
		return make_response(InternalServerError(),500)
	temp={"LangId":"", "Lang":""}
	final=[]
	for lan in AllLanguages:
		temp["LangId"] = lan.Language_id
		temp["Lang"] = lan.Name
		final.append(temp)
		temp={"LangId":"", "Lang":""}
	del temp
	return make_response(CreatePayload({"status":"True", "message":"payload contains all data"},final),200)


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
		application.logger.debug(str(e))
		return make_response(InternalServerError(),500)
	return make_response(CreatePayload({"status":True, "message":"Language added successfully"},None),200)
