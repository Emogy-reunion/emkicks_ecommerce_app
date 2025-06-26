from flask import url_for, render_template
from flask_mail import Message, Mail
from create_app import create_app

app = create_app()
mail = Mail(app)

def send_verification_email(user):
    '''
    sends an email with the verification token to the user
    '''
    try:
        verification_token = user.generate_email_verification_token()
        verification_url = url_for('https://mark.com/verify', verification_token=verification_token, _external=True)

        msg = Message(
                subject='VERIFY YOUR EMAIL!',
                recipients=[user.email],
                sender='info.bytevision@gmail.com'
                )
        msg.body = f"Click the following link to verify your email: {verification_url}. The link expires in 60 minutes"
        msg.html = render_template('verification.html', username=user.username)
        mail.send(msg)
    except Exception as e:
        return jsonify({"error": 'An unexpected error occured. Please try again!'}), 500
