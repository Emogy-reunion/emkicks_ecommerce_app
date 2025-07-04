'''
Initializes the tables
Hash passwords
'''
from core import db, create_app, bcrypt
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime


serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

class Users(db.Model):
    '''
    stores user information about a specific user
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default='member')
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sneakers = db.relationship('Sneakers', back_populates='user', lazy='select', cascade='all, delete-orphan')
    jerseys = db.relationship('Jerseys', back_populates='user', lazy='select', cascade='all, delete-orphan')
    cart = db.relationship('Cart', back_populates='user', uselist=False, cascade='all, delete-orphan', lazy='select')


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
        '''i
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
    Has a one to many relationship with the Images model - one post can have
        multiple images
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    original_price = db.Column(db.Float, nullable=False)
    discount_rate = db.Column(db.Integer, default=0)
    final_price = db.Column(db.Float, nullable=False)
    size = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('Users', back_populates='sneakers')
    images = db.relationship('Images', back_populates='sneaker', lazy='select', cascade='all, delete-orphan')

    def __init__(self, name, original_price, discount_rate, brand,
                 user_id, final_price, size, status, description, category):
        '''
        initializes the table with data
        '''
        self.name = name
        self.user_id = user_id
        self.original_price = original_price
        self.discount_rate = discount_rate
        self.final_price = final_price
        self.size = size
        self.status = status
        self.description = description
        self.category = category
        self.brand = brand

class Images(db.Model):
    '''
    stores the image filenames for the sneakers
    Has many to one relationship with the Sneakers model - multiple images
        can be related to one image
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    sneaker_id = db.Column(db.Integer, db.ForeignKey('sneakers.id'), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    sneaker = db.relationship('Sneakers', back_populates='images', lazy=True)

    def __init__(self, sneaker_id, filename):
        '''
        initializes the images table with data
        '''
        self.sneaker_id = sneaker_id
        self.filename = filename

class Jerseys(db.Model):
    '''
    stores the jersey information
    has a one to many relationship with the JerseyImages table
        one jersey can have multiple images
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    jersey_type = db.Column(db.String(150), nullable=False)
    original_price = db.Column(db.Float, nullable=False)
    discount_rate = db.Column(db.Integer, default=0)
    final_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    season = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('Users', back_populates='jerseys')
    images = db.relationship('JerseyImages', back_populates='jersey', lazy='select', cascade='all, delete-orphan')

    def __init__(self, name, jersey_type, original_price, discount_rate,
                 user_id, final_price, season, status, size, description):
        '''
        initializes the table with data
        '''
        self.name = name
        self.user_id = user_id
        self.jersey_type = jersey_type
        self.original_price = original_price
        self.discount_rate = discount_rate
        self.final_price = final_price
        self.status = status
        self.size = size
        self.description = description
        self.season = season

class JerseyImages(db.Model):
    '''
    stores images related to a certain jersey
    has a many to one relationship with the Jerseys table
        multiple images can belong to one jersey
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    jersey_id = db.Column(db.Integer, db.ForeignKey('jerseys.id'), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    jersey = db.relationship('Jerseys', back_populates='images')

    def __init__(self, jersey_id, filename):
        '''
        initialize the table with data
        '''
        self.jersey_id = jersey_id
        self.filename = filename


class Cart(db.Model):
    '''
    the users cart
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('Users', back_populates='cart')
    cart_items = db.relationship('CartItems', backref='cart', lazy='select', cascade='all, delete-orphan')

    def __init__(self, user_id):
        '''
        initializes the cart with data
        '''
        self.user_id = user_id

class CartItems(db.Model):
    '''
    stores the cart items
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    cart_id = db.Column(db.Integer,db.ForeignKey('cart.id'), nullable=False)
    product_type = db.Column(db.String(50), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(50), nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    sneakers = db.relationship('Sneakers', backref='sneaker_cart_items')
    jerseys = db.relationship('Jerseys', backref='jersy_cart_items')

    def __init__(self, cart_id, product_type, product_id, quantity,
                 price, size, subtotal):
        '''
        initializes the cart items table with data
        '''
        self.cart_id = cart_id
        self.product_type = product_type,
        self.product_id = product_id,
        self.quantity = quantity,
        self.size = size,
        self.subtotal = subtotal
