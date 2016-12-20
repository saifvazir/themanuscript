
from migrate.versioning import api
from application import application

api.upgrade(application.config['SQLALCHEMY_DATABASE_URI'], application.config['SQLALCHEMY_MIGRATE_REPO'])
v = api.db_version(application.config['SQLALCHEMY_DATABASE_URI'], application.config['SQLALCHEMY_MIGRATE_REPO'])
print('Current database version: ' + str(v))