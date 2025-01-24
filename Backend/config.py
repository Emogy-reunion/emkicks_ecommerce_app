'''
stores the app's configuration settings
'''
from dotenv import load_dotenv
import os


class Config():
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
