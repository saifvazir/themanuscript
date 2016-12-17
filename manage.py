import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from app import app
from models import tmsdb
import config


app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, tmsdb)
manager = Manager(app)

manager.add_command('tmsdb', MigrateCommand)


if __name__ == '__main__':
    manager.run()
