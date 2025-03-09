from flask import Blueprint, jsonify, request
from model import Users, db
from email_validator import validate_email, EmailNotFoundError
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies
from utils.verification_email import send_verification_email
from utils.validatation import validate_firstname, validate_lastname, check_email


auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    '''
    allows user to create accounts
    '''
    data = request.json

    firstname = data['firstname']
    lastname = data['lastname']
    email = data['email']
    username = data['username']
    phone = data['phone']
    password = data['password']

    errors = {}
    firstname_errors = validate_firstname(firstname)
    lastname_errors = validate_lastname(lastname)
    email_errors = check_email(email)

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

    
