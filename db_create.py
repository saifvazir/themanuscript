# from application.models import Data
from migrate.versioning import api
# from config import SQLALCHEMY_DATABASE_URI
# from config import SQLALCHEMY_MIGRATE_REPO
from application import application
from application import db
from application import models
import os.path
db.create_all()
db.session.commit()
if not os.path.exists(application.config['SQLALCHEMY_MIGRATE_REPO']):
    api.create(application.config['SQLALCHEMY_MIGRATE_REPO'], 'database repository')
    api.version_control(application.config['SQLALCHEMY_DATABASE_URI'], application.config['SQLALCHEMY_MIGRATE_REPO'])
else:
    api.version_control(application.config['SQLALCHEMY_DATABASE_URI'], application.config['SQLALCHEMY_MIGRATE_REPO'], api.version(application.config['SQLALCHEMY_MIGRATE_REPO']))