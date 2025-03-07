from flask import Blueprint, jsonify, request
from model import Users, db
from email_validator import validate_email, EmailNotFoundError
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies
from utils.verification_email import send_verification_email


auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    '''
    allows user to create accounts
    '''
    RESERVED_USERNAMES = ['root', 'admin', 'moderator', 'support', 'null', 'undefined']
    data = request.json

    firstname = data['firstname']
    lastname = data['lastname']
    email = data['email']
    username = data['username']
    phone = data['phone']
    password = data['password']

    errors = {}
    
    if not firstname:
        errors['firstname'] = 'First name is required!'
    elif len(firstname) < 2:
        errors['firstname'] = 'First name is too short. First name should be 2 or more characters long!'
    elif len(firstname) > 50:
        errors['firstname'] = 'First name is too long. First name should be less than 50 characters long!'

    if not lastname:
        errors['lastname'] = 'Last name is required!'
    elif len(lastname) < 2:
        errors['lastname'] = 'Last name is too short. Last name should be 2 or more characters long!'
    elif len(lastname) > 50:
        errors['lastname'] = 'Last name is too long. Lastname name should be less than 50 characters long!'

    if not email:
        errors['email'] = 'Email is required!'
    elif len(email) < 5:
        errors['email'] = 'Email is too short. It should be more than 5 characters!'
    elif len(email) > 50:
        errors['email'] = 'Email is too long. It should not exceed 50 characters!'
    else:
        try:
            valid = validate_email(email, check_delivaribility=True)
        except EmailNotValidError as e:
            errors['email'] = 'Invalid email format!'

    if not username:
        errors['username'] = 'Username is required!'
    elif len(username) < 5:
        errors['username'] = 'Username is too short. Username should be 5 or more characters long!'
    elif len(username) > 50:
        errors['username'] = 'Username is too long. Username should not exceed 50 characters'
    elif username.lower() in RESERVED_USERNAMES:
        errors['username'] = 'Username is associated with another account, please pick another one!'





    user = Users.query.filter_by(email=email).first()
    member = Users.query.filter_by(username=username).first()

    if user:
        return jsonify({'error': 'An account associated with this email exists!'})
    elif member:
        return jsonify({'error': 'An account associated with this username exists!'})
    else:
        try:
            new_user = Users(firstname=firstname, lastname=lastname,
                             email=email, username=username, phone=phone,
                             password=password)
            db.session.add(new_user)
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'An unexpected error occured. Please try again!'})

        db.session.commit()
        send_verification_email(new_user)
        return jsonify({'success': 'Account created successfully!. Click the link sent to your email to verify you identity!'})

@auth.route('/login', methods=['POST'])
def login():
    '''
    authenticate the user
    logs them in to the session
    '''
    data = request.json

    identifier = data['identifier']
    password = data['password']

    user = None

    if '@' in identifier:
        user = Users.query.filter_by(email=identifier).first()

        if not user:
            return jsonify({'error': 'The email you entered does not match any account!'})
    else:
        user = Users.query.filter_by(username=identifier).first()

        if not user:
            return jsonify({'error': 'The username you entered does not match any account!'})

    if user.check_passwordhash(password):
        '''
        verifies the user password
        if correct it creates and returns access token
        if incorrect it returns an error message
        '''
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        response = jsonify({'success': ' Successfully logged in!'})
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response
    else:
        return jsonify({'error': 'Incorrect password. Please try again!'})

    
