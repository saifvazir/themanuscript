from models import Books, tmsdb, Count
from TMS import app

def increasebookscount():
	result = Count.query.all()[0]
	result.bookscount += 1
	try:
		tmsdb.session.commit()
	except:
		print "error occured"


def generatebookid(title):
	temp = '#BOBJ'
	temp += str(len(title))[0]
	noofusers = ""
	try:
		noofbooks = Count.query.with_entities(Count.bookscount)
		print "awegrtyui"
	except:
		print "query not successfull"
	temp += str(noofbooks[0][0]+1)
	return temp