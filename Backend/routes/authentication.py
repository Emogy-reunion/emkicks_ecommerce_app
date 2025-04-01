from flask import Blueprint, jsonify, request
from models import Users, db
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies, get_jwt_identity, jwt_required
from utils.verification_email import send_verification_email
from utils.validation import validate_firstname, validate_lastname, check_email


auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    '''
    allows user to create accounts
    '''
    data = request.json

    firstname = data['firstname'].lower()
    lastname = data['lastname'].lower()
    email = data['email'].lower()
    username = data['username'].lower()
    phone = data['phone']
    password = data['password']

    errors = {}
    firstname_errors = validate_firstname(firstname)
    lastname_errors = validate_lastname(lastname)
    email_errors = check_email(email)

    if firstname_errors:
        errors['firstname'] = firstname_errors

    if lastname_errors:
        errors['lastname'] = lastname_errors

    if email_errors:
        errors['email'] = email_errors

    if errors:
        return jsonify({'errors': errors}), 400

    user = Users.query.filter_by(email=email).first()
    member = Users.query.filter_by(username=username).first()

    if user:
        return jsonify({'error': 'An account associated with this email exists!'}), 409
    elif member:
        return jsonify({'error': 'An account associated with this username exists!'}), 409
    else:
        try:
            new_user = Users(firstname=firstname, lastname=lastname,
                             email=email, username=username, phone=phone,
                             password=password)
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
        send_verification_email(new_user)
        return jsonify({'success': 'Account created successfully!. Click the link sent to your email to verify you identity!'}), 201

@auth.route('/login', methods=['POST'])
def login():
    '''
    authenticate the user
    logs them in to the session
    '''
    data = request.json

    identifier = data['identifier'].lower()
    password = data['password']

    user = None

    if '@' in identifier:
        user = Users.query.filter_by(email=identifier).first()

        if not user:
            return jsonify({'error': 'The email you entered does not match any account!'}), 404
    else:
        user = Users.query.filter_by(username=identifier).first()

        if not user:
            return jsonify({'error': 'The username you entered does not match any account!'}), 404

    if user.check_passwordhash(password):
        '''
        verifies the user password
        if correct it creates and returns access token
        if incorrect it returns an error message
        '''
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        response = jsonify({'success': ' Successfully logged in!'}), 200
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response
    else:
        return jsonify({'error': 'Incorrect password. Please try again!'}), 401

@auth.route('/logout', methods=['POST'])
def logout():
    '''
    logs out the user by destroying the jwt cookies
    '''
    response = jsonify({'success': 'Successfully logged out!'}), 200
    unset_jwt_cookies(response)
    return response

@jwt_required(refresh=True)
@auth.route('/refresh_token', methods=['POST'])
def refresh_token():
    '''
    renews an access token after it expires
    '''
    user_id = get_jwt_identity()
    response = ({'success': 'Access cookies refreshed successfully!'}), 200
    set_jwt_access_cookies(response)
    return response
