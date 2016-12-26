
from flask import request,make_response
from application.api.Genres.functions import *
from application.models import Genres
import json
from application.api.Users.functions import InternalServerError
from application import db
from application import CreatePayload
from application import application

from application.api.Genres import genres
#api to get all the languages
@genres.route('/api/v1.0/get_genres')
def get_genres():

	try:
		AllGenres = Genres.query.all()
	except Exception as e:
		application.logger.debug(str(e))
		return make_response(InternalServerError(),500)
	temp={"GenId":"", "Genre":""}
	final=[]
	for Genre in AllGenres:
		temp["GenId"] = Genre.Genre_id
		temp["Genre"] = Genre.Genre_type
		final.append(temp)
		temp={"GenId":"", "Genre":""}
	del temp
	return make_response(CreatePayload({"status":"True", "message":"payload contains all data"},final),200)


#apis for admin to add one language at a time
#auth required
@genres.route('/api/v1.0/add_genre',methods=['POST'])
def add_genres():
	data = json.loads(request.data)["payload"]
	GType = data['genre']
	temp = GenerateGenreId(GType)
	Genre_id = temp["temp"]
	id = temp["count"]
	new_entry = Genres(id,Genre_id,GType)
	try:
		db.session.add(new_entry)
		db.session.commit()
		increasegenrescount()
	except Exception as e:
		application.logger.debug(str(e))
		return make_response(InternalServerError(),500)
	return make_response(CreatePayload({"status":True, "message":"Genre added successfully"},None),200)
