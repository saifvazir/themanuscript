
from flask import Flask, jsonify
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


@application.route('/')
def index():
	return "site under construction"


@application.errorhandler(404)
def page_not_found(e):
	return jsonify({"payload": {
		"success": False,
		"error_code": 404,
		"error_desc": "page not found"
	}})


@application.errorhandler(500)
def internal_server_error(e):
	return jsonify({"payload": {
		"success": False,
		"error_code": 500,
		"error_desc": "internal server error"
	}})


if __name__ == '__main__':
	application.run(host='0.0.0.0')
