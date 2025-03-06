'''
allows users to reset their passwords
'''
from flask import Blueprint, request, jsonify
from model import Users
from utils.password_reset_email import send_password_reset_email


reset = Blueprint('reset', __name__)

@reset.route('/reset_password', methods=['POST'])
def reset_password_token():
    '''
    sends the user a password reset email
    '''
    data = request.json
    email = data['email']

    user = Users.query.filter_by(email=email).first()

    if user:
        send_password_reset_email(user)
        return jsonify({'success': 'Password reset email sent! Check your inbox or spam folder to reset your password.'})
    else:
        return jsonify({'error': 'The email you entered does not match any account!'})

