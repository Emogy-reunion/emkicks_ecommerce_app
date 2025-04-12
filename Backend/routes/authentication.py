from flasik import Blueprint, jsonify, request
from models import Users, db
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies, get_jwt_identity, jwt_required
from utils.verification_email import send_verification_email
from form import RegistrationForm, LoginForm


auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    '''
    allows user to create accounts
    '''
    form = RegistrationForm(data=request.get_json)

    if form.validate():
        firstname = form.firstname.data.lower()
        lastname = form.lastname.data.lower()
        username = form.username.data.lower()
        email = form.email.data.lower()
        password = form.email.data


        user = None
        member = None

        try:
            user = Users.query.filter_by(email=email).first()
            member = Users.query.filter_by(username=username).first()
        except Exception as e:
            return jsonify({'error': 'An unexpected error occured. Please try again'}), 500

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
    else:
        return jsonify({'errors': form.errors}), 400


@auth.route('/login', methods=['POST'])
def login():
    '''
    authenticate the user
    logs them in to the session
    '''
    form = LoginForm(request.get_json)

    if form.validate():
        identifier = form.identifier.data.lower()
        password = form.password.data

        user = None

        if '@' in identifier:
            try:
                user = Users.query.filter_by(email=identifier).first()
            except Exception as e:
                return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500

            if not user:
                return jsonify({'error': 'The email you entered does not match any account!'}), 404
        else:
            try:
                user = Users.query.filter_by(username=identifier).first()
            except Exception as e:
                return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500

            if not user:
                return jsonify({'error': 'The username you entered does not match any account!'}), 404

        if user.check_passwordhash(password):
            '''
            verifies the user password
            if correct it creates and returns access token
            if incorrect it returns an error message
            '''
            try:
                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)

                response = jsonify({'success': ' Successfully logged in!'}), 200
                set_access_cookies(response, access_token)
                set_refresh_cookies(response, refresh_token)
                return response
            except Exception as e:
                return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
        else:
            return jsonify({'error': 'Incorrect password. Please try again!'}), 400
    except Exception as e:
        return jsonify({'errors': form.errors})

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
