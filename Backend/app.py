'''
initializes the libraries
creates initial admins
runs the application
registers the blueprints
'''
from create_app import create_app
from routes.authentication import auth
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from utils.create_upload_folder import create_upload_folder
from routes.verification import verify
from routes.reset_password import reset
from routes.upload import post
from routes.user_search import find
from routes.user_collections import posts



app = create_app()
jwt = JWTManager(app)

app.register_blueprint(auth)
app.register_blueprint(verify)
app.register_blueprint(reset)
app.register_blueprint(post)
app.register_blueprint(posts)
app.register_blueprint(find)

create_upload_folder()

if __name__ == '__main__':
        app.run(debug=True)
