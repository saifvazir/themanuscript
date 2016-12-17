from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from application import db
from application.api.Users.views import users
from application import models
# import config

application = Flask(__name__)
CORS(application)

application.register_blueprint(users)

application.config.from_object('config.TestingConfig')
# os.environ['APP_SETTINGS'] = 'config.DevelopmentConfig'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ankitesh:postgres@localhost/themanuscript'


# @app.route('/')
# def hello():
#     return "Hello World!"


@application.route('/')
def hello_name():
    return "site under construction"


if __name__ == '__main__':
    application.run(host='0.0.0.0')

