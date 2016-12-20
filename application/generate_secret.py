
from models import SecretKeys
import db
import random
import string

text = string.digits+string.letters

for i in range(10):
	key = "".join([random.choice(text) for j in range(20)])
	new_key = SecretKeys(i, key)
	try:
		db.session.add(new_key)
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		raise e