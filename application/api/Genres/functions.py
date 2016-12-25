
from application.models import Count
from application import db

def GenerateGenreId(genres):
	temp = '#GOBJ'
	temp += str(len(genres))
	noofgenres = ""
	try:
		noofgenres = Count.query.with_entities(Count.genrescount).first()
	except Exception as e:
		print str(e)
		raise e
	a = noofgenres[0]
	temp += str(noofgenres[0]+1)
	del noofgenres
	return {"count":a+1, "temp":temp}

def increasegenrescount():
	result = Count.query.all()[0]
	result.genrescount += 1
	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(str(e))
		raise e

#Genres types
# Book categories
# Adventure
# Astounding Stories
# Crime fiction
# Crime non fiction
# Detective fiction
# Fantasy
# Humor
# Horror
# Movie books
# Mystery
# Mythology
# Philosophy
# Poetry
# Romantic
# Science fiction
# School stories
# Children's myths fairytales