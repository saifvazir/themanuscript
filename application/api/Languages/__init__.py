
from flask import Blueprint
languages = Blueprint('languages', __name__)
from . import views