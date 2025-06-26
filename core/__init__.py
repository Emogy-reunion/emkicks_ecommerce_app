from flask import Flask
from config import Config
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
'''
creates the application instance
initializes it with the configuration settings
'''

bcrypt = Bcrypt()
db = SQLAlchemy()
mail = Mail()


def create_app():
    '''
    creates the application instance and returns it
    '''
    app = Flask(__name__)
    app.config.from_object(Config)

    bcrypt.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    return app
