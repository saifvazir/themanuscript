import imp
from migrate.versioning import api
from application import db
from application import application
# from config import SQLALCHEMY_DATABASE_URI
# from config import SQLALCHEMY_MIGRATE_REPO
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
# v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(application.config['SQLALCHEMY_DATABASE_URI'], application.config['SQLALCHEMY_MIGRATE_REPO'])
migration = application.config['SQLALCHEMY_MIGRATE_REPO'] + ('/versions/%03d_migration.py' % (v+1))
tmp_module = imp.new_module('old_model')
old_model = api.create_model(application.config['SQLALCHEMY_DATABASE_URI'], application.config['SQLALCHEMY_MIGRATE_REPO'])
exec old_model in tmp_module.__dict__
script = api.make_update_script_for_model(application.config['SQLALCHEMY_DATABASE_URI'],
                                          application.config['SQLALCHEMY_MIGRATE_REPO'],
                                          tmp_module.meta, db.metadata)
open(migration, "wt").write(script)
api.upgrade(application.config['SQLALCHEMY_DATABASE_URI'], application.config['SQLALCHEMY_MIGRATE_REPO'])
v = api.db_version(application.config['SQLALCHEMY_DATABASE_URI'], application.config['SQLALCHEMY_MIGRATE_REPO'])
print('New migration saved as ' + migration)
print('Current database version: ' + str(v))
