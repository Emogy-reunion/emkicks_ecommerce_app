from flask import url_for, render_template
from create_app import create_app
from flask_mail import Message, Mail

app = create_app()
mail = Mail(app)

def send_password_reset_email(user):
    '''
    sends a link to change the user password via email
    '''
    try:
        token = user.generate_email_verification_token()
        verification_url = url_for('https://mark.com/reset_password', token=token, _external=True)

        msg = Message(
                subject='Reset your password',
                recipients=[user.email],
                sender='info.bytevision@gmail.com'
                )
        msg.body= f"Click the following link to reset your password: {verification_url}. The link expires in 60 minutes."
        msg.html = render_template('reset_password.html', username=user.username)
        mail.send(msg)
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again'})
