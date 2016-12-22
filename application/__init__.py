from flask import Flask,g,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as JWT
import json
import datetime
application = Flask(__name__)
application.config.from_object('config.TestingConfig')
db = SQLAlchemy(application)
import models
jwt = JWT(application.config['SECRET_KEY'], expires_in=172800)
auth  = HTTPTokenAuth('Bearer')

@auth.verify_token
def verify_token(token):
    temp = json.loads(token)
    token = temp["token"]
    id = temp["id"]
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
    return jsonify({"payload":{
    	"success": False,
    	"error_code":401,
    	"error_message":"Unauthorized"
    	}})

def CreatePayload(success, payload, error=None ):
    if error:
        return jsonify({"success":success, "payload":payload, "error":error})
    return jsonify({"success":success, "payload":payload})