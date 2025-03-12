'''
Initializes the tables
Hash passwords
'''
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from create_app import create_app
from itsdangerous import URLSafeTimedSerializer


app = create_app()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

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
    verified = db.Column(db.Boolean, default=False)

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

    def check_passwordhash(self, password):
        '''
        compares the user password and the stored hash
        '''
        return bcrypt.check_password_hash(self.password, password)

    def generate_email_verification_token(self):
        '''
        serializes the user id and returns it
        '''
        return serializer.dumps({'user_id': self.id}, expires_in=3600)
    
    @staticmethod
    def verify_email_verification_token(token):
        '''
        deserializes the token and extracts the user id
        searches for the user in the database
        if user exists it returns success message
        '''
        try:
            data = serializer.loads(token, max_age=3600)
            return db.session.get(Users, data['user_id'])
        except Exception as e:
            return None


class Sneakers(db.Model):
    '''
    stores the sneaker information
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def __init__(self, name, price, size, status, description, category):
        '''
        initializes the table with data
        '''
        name = self.name
        price = self.price
        size = self.price
        status = self.status
        description = self.description
        category = self.category

class Images(db.Model):
    '''
    stores the image filenames for the sneakers
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    filename = db.Column(db.String(200), nullable=False)
