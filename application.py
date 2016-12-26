
from flask import Flask, jsonify,make_response
from flask_cors import CORS

from application.api.Users.views import users
from application.api.Languages.views import languages
from application.api.Genres.views import genres

application = Flask(__name__)
CORS(application)

application.register_blueprint(users)
application.register_blueprint(languages)
application.register_blueprint(genres)

application.config.from_object('config.TestingConfig')

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


if __name__ == '__main__':
	application.run(host='0.0.0.0')
