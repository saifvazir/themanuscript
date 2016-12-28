
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as JWT
import json
import datetime
from flask import Flask, jsonify,make_response
from flask_cors import CORS

application = Flask(__name__)
CORS(application)
application.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(application)
import models

jwt = JWT(application.config['SECRET_KEY'], expires_in=172800)
auth = HTTPTokenAuth('Bearer')


@auth.verify_token
def verify_token(token):
    temp = token
    temp_list = temp.split('.')
    id = temp_list[-1]
    del temp_list
    try:
        user = models.Users.query.filter_by(User_id=id).first()
    except Exception as e:
        print(str(e))
        return False
    if not user:
        return False
    tokens = user.tokens
    if not tokens:
        return False
    user_tokens = json.loads(tokens)["payload"]
    now = str(datetime.datetime.now())
    search = filter(lambda tok: tok['token'] == token and tok['expiration'] >= now, user_tokens)[0]
    if not search:
        return False
    return True

@auth.error_handler
def auth_error():
    return make_response(jsonify({"payload":{
    	"success": False,
    	"error_code":401,
    	"error_message":"Unauthorized"
    	}}),401)

def CreatePayload(success, payload, error=None ):
    if error:
        return jsonify({"success":success, "payload":payload, "error":error})
    return jsonify({"success":success, "payload":payload})



from application.api.Users import users
from application.api.Languages import languages
from application.api.Genres import genres
application.register_blueprint(users)
application.register_blueprint(languages)
application.register_blueprint(genres)

if not application.debug:
	import logging
	from logging.handlers import RotatingFileHandler
	file_handler = RotatingFileHandler('tmp/tms.log', 'a', 1 * 1024 * 1024, 10)
	file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	application.logger.setLevel(logging.DEBUG)
	file_handler.setLevel(logging.DEBUG)
	application.logger.addHandler(file_handler)
	application.logger.info('tms startup')


@application.route('/')
def index():
	return "site under construction"

@application.errorhandler(404)
def page_not_found(e):
	return make_response(jsonify({"payload": {
		"success": False,
		"error_code": 404,
		"error_desc": "page not found"
	}}),404)


@application.errorhandler(500)
def internal_server_error(e):
	return make_response(jsonify({"payload": {
		"success": False,
		"error_code": 500,
		"error_desc": "internal server error"
	}}),500)




