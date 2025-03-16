'''
Handles token verification via email
'''
from flask import Blueprint, jsonify
from model import db, Users

verify = Blueprint('verify', __name__)

@verify.route('/verify_email/<token>', methods=['POST'])
def verify_email(token):
    '''
    checks if the token is valid
    updates the user verification status to true if the token is valid
    '''
    user = Users.verify_email_verification_token(token)

    if user:
        try:
            user.verified = True
        except Exception as e:
            return jsonify({'error': 'An unexpected error occured. Please try again later!'}), 500
        db.session.commit()
        return jsonify({'success': 'Your account has been verified successfully!'}), 200
    else:
        return jsonify({'error': ' Verification token has expired. Please request a new one!'}), 403
