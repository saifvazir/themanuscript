
from flask import request,Blueprint
from application.api.Genres.functions import *
from application.models import Genres
import json
from application.api.Users.functions import InternalServerError
from application import db
from application import CreatePayload


genres = Blueprint('genres', __name__)

#api to get all the languages
@genres.route('/api/v1.0/get_genres')
def get_genres():

	try:
		AllGenres = Genres.query.all()
	except Exception as e:
		print str(e)
		return InternalServerError()
	temp={"GenId":"", "Genre":""}
	final=[]
	for Genre in AllGenres:
		temp["GenId"] = Genre.Genre_id
		temp["Genre"] = Genre.Genre_type
		final.append(temp)
		temp={"GenId":"", "Genre":""}
	del temp
	return CreatePayload({"status":"True", "message":"payload contains all data"},final)


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
		print str(e)
		return InternalServerError()
	return CreatePayload({"status":True, "message":"Genre added successfully"},None)
