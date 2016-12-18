from flask import Flask,jsonify
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
def index():
    return "site under construction"


@application.errorhandler(404)
def page_not_found(e):
	return jsonify({"payload":{
		"success":False,
		"error_code":404
		"error_desc":"page not found"
		}})

@application.errorhandler(500)
def internal_server_error(e):
	return jsonify({"payload":{
		"success":False,
		"error_code":500
		"error_desc":"internal server error"
		}})




if __name__ == '__main__':
    application.run(host='0.0.0.0')

