'''
initializes the libraries
creates initial admins
runs the application
registers the blueprints
'''
from Backend import create_app
from Backend.routes.authentication import auth
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from utils.create_upload_folder import create_upload_folder
from Backend.routes.verification import verify
from Backend.routes.reset_password import reset
from Backend.routes.upload import post
from Backend.routes.user_search import user_search_bp
from Backend.routes.member_search import member_search_bp
from Backend.routes.user_collections import user_posts_bp
from Backend.routes.member_collections import member_posts_bp
from Backend.routes.cart import cart
from Backend.routes.member_profiles import member_profile_bp



app = create_app()
jwt = JWTManager(app)

app.register_blueprint(auth)
app.register_blueprint(verify)
app.register_blueprint(reset)
app.register_blueprint(post)
app.register_blueprint(user_posts_bp)
app.register_blueprint(member_posts_bp)
app.register_blueprint(user_search_bp)
app.register_blueprint(member_search_bp)
app.register_blueprint(cart)
app.register_blueprint(member_profile_bp)

create_upload_folder()

if __name__ == '__main__':
    '''
    runs the application
    '''
    app.run(debug=True)
