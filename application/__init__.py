from flask import Flask,g,jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as JWT

application = Flask(__name__)
application.config.from_object('config.TestingConfig')
db = SQLAlchemy(application)

jwt = JWT(application.config['SECRET_KEY'], expires_in=172800)
auth  = HTTPTokenAuth('Bearer')

@auth.verify_token
def verify_token(token):
    g.user = None
    try:
        data = jwt.loads(token)
    except:
        return False
    if 'id' in data:
        g.user = data['id']
        return True

    return False

@auth.error_handler
def auth_error():
    return jsonify({"payload":{
    	"success": False,
    	"error_code":401,
    	"error_message":"Unauthorized"
    	}})