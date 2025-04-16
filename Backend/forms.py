'''
an initialization of all the application's forms
'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, FloatField, MultipleFileField
from wtf.validators import DataRequired, Email, Length, InputRequired, Regexp, EqualTo, NumberRange


class RegistrationForm(FlaskForm):
    '''
    initializes the registration form
    validates the registration forms input
    '''
    firstname = StringField('First name', validators=[
        DataRequired(),
        Length(min=2, max=30, message='First name must be between 2 and 30 characters!')])
    lastname = StringField('Last name', validators=[
        DataRequired(),
        Length(min=2, max=30, message='Last name must be between 2 and 30 characters!')])
    email = StringField('Email', validators=[
        InputRequired(),
        Email(),
        Length(min=4, max=45, message='Email must be between 4 and 45 characters!')])
    Username = StringField(
            'Username', validators=[
                DataRequired(message="Username is required"),
                Length(min=3, max=25, message="Username must be between 3 and 25 characters"),
                Regexp('^\w+$', message="Username must contain only letters, numbers, or underscores")])
    phone_number = StringField('Phone number', validators=[
        InputRequired(),
        Regexp(r'^\+2547\d{8}$', message="Phone number must start with +2547 followed by 8 digits.")
        ])
    password = PasswordField('Password', validators=[
        InputRequired(),
        Length(min=8, message="Password must be at least 8 characters long."),
        Regexp(r'(?=.*[A-Z])', message="Password must contain at least one uppercase letter."),
        Regexp(r'(?=.*[a-z])', message="Password must contain at least one lowercase letter."),
        Regexp(r'(?=.*\W)', message="Password must contain at least one special character.")
        ])
    confirmpassword = PasswordField('Confirm password', validators=[InputRequired(), EqualTo('password', message='Passwords must match!')])

class LoginForm(FlaskForm):
    '''
    initializes the login form fields
    validates the login form data
    '''
    identifier = StringField('Email/Username', validators = [
        DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])


class SneakerUploadForm(FlaskForm):
    '''
    validates the upload form fields
    '''
    name = StringField('Sneaker name', validators=[
        DataRequired(),
        Length(min=4, max=45, message='Sneaker name must be betwwen 4 and 45 characters!')])
    original_price = FloatField('Original price', validators=[
        DataRequired(),
        NumberRange(min=0)])
    discount_rate = IntegerField('Discount rate', validators=[
        DataRequired(),
        NumberRange(min=0, max=99)])
    description = TextField('Description', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()])
    size = StringField('Size', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    brand = StringField('Brand', validators=[DataRequired()])
    files = MultipleFileField('Images', validators=[DataRequired()])

class JerseyUploadForm(FlaskForm):
    '''
    validates the sneaker upload form fields
    '''
    name = StringField('Jersey team name', validators=[
        DataRequired(),
        Length(min=4, max=45, message='Sneaker name must be betwwen 4 and 45 characters!')])
     original_price = FloatField('Original price', validators=[
         DataRequired(),
         NumberRange(min=0)])
     discount_rate = IntegerField('Discount rate', validators=[
         DataRequired(),
         NumberRange(min=0, max=99)])
     description = TextField('Description', validators=[DataRequired()])
     status = StringField('Status', validators=[DataRequired()])
     size = StringField('Size', validators=[DataRequired()])
     season = StringField('Season', validators=[DataRequired()])
     jersey_type = StringField('Jersey type', validators=[DataRequired()])
     files = MultipleFileField('Images', validators=[DataRequired()])

class SneakerSizeQuantityForm(FlaskForm):
    '''
    validates the sneaker size
    '''
    size = StringField('Size', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[
        DataRequired(),
        NumberRange(min=1, message='43')])

class JerseySizeQuantityForm(FlaskForm):
    '''
    validates the sneaker size
    '''
    size = StringField('Size', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[
        DataRequired(),
        NumberRange(min=1, message='43')])

class SneakerSearchForm(FlaskForm):
    '''
    validates the logged out users sneakers search form
    '''
    name = StringField('Name', validators=[
        Optional(),
        Length(max=50, message='Maximum length must not exceed 50 characters!'}
        ])
    minimum_price = FloatField('Minimum price', validators=[
        Optional(),
        NumberRange(min=0, message='Minimum price must not be below 0!')
        ])
    maximum_price = FloatField('Maximum price', validators=[
        Optional(),
        NumberRange(min=0, message='Maximum price must not be below 0!')
        ])
    category = StringField('Category', validators=[
        Optional(),
        Length(Max=10, message='Category length must not exceed 10 characters!')
        ])
    size = StringField('Size', validators=[
        Optional(),
        NumberRange(min=34, message='Sneaker size cannot be below 34!')])
    brand = StringField('Brand', validators=[
        Optional(),
        Length(max=50, message='Maximum length must not exceed 25 characters!'})
        ])
