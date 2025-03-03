from flask import Blueprint
from model import Users, db
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, jsonify


auth = Blueprint('auth', __main__)

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


    user = Users.query.filter_by(email=email).first()

    if user:
        return jsonify({'error': 'An account associated with this email exists'})
    else:
        try:
            new_user = Users(firstname=firstanme, lastname=lastname,
                             email=email, username=username, phone=phone,
                             password=password)
            db.session.add(new_user)
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'An unexpected error occured. Please try again'})

        db.session.commit()
        return jsonify({'success': 'Account created successfully!'})
