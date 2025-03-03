from flask import Flask
from config import Config
'''
creates the application instance
initializes it with the configuration settings
'''


def create_app():
    '''
    creates the application instance and returns it
    '''
    app = Flask(__name__)
    app.config.from_object(Config)
    return app
