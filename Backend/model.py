'''
Initializes the tables
'''
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from create_app import create_app


app = create_app()
db = SQLAlchemy(db)
bcrypt = Bcrypt(app)

class Users(db.Model):
    '''
    stores user information
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default='guest')

    def __init__(firstname, lastname, email, username, phone, password):
        '''
        initializes the tables with data
        '''
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = username
        self.phone = phone
        self.password = self.generate_passwordhash(password)

    def generate_passwordhash(self, password):
        '''
        hashes the password to ensure that it is secure
        '''
        return bcrypt.generate_password_hash(password)
