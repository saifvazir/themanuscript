
from application.models import Count
from application import db

def GenerateLanguageId(language):
	temp = '#LOBJ'
	temp += str(language[0:3])
	nooflanguages = ""
	try:
		nooflanguages = Count.query.with_entities(Count.languagescount).first()
	except Exception as e:
		print str(e)
		raise e
	a = nooflanguages[0]
	temp += str(nooflanguages[0]+1)
	del nooflanguages
	return {"count":a+1, "temp":temp}

def increaselanguagescount():
	result = Count.query.all()[0]
	result.languagescount += 1
	try:
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(str(e))
		raise e

#languages
# Hindi Bengali Marathi Gujarati Tamil Telugu English