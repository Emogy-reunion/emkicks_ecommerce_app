from flask import Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies


auth = Blueprint('auth', __main__)
