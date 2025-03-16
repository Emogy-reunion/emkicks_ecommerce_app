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
        return jsonify({'success': 'Password reset email sent! Check your inbox or spam folder to reset your password.'}), 200
    else:
        return jsonify({'error': 'The email you entered does not match any account!'}), 409



@reset.route('/update_password/<token>', methods=['POST'])
def update_password(token):
    '''
    checks if the token is valid and updates the user password
    '''
    data = request.json
    password = data['password']

    user = Users.verify_email_verification_token(token)
    
    if user:
        try:
            user.password = user.generate_password(password)
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'An unexpected error has occured. Please try again!'}), 500
        db.session.commit()
        return jsonify({'success': 'Password updated successfully!'}), 200
    else:
        return jsonify({'error': 'Verification token is invalid. Please request a new one!'}), 403
