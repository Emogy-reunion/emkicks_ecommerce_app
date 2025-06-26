'''
initializes the libraries
creates initial admins
runs the application
registers the blueprints
'''
from core import create_app
from core.routes.authentication import auth
from core.utils.create_upload_folder import create_upload_folder
from core.routes.verification import verify
from core.routes.reset_password import reset
from core.routes.upload import post
from core.routes.user_search import user_search_bp
from core.routes.member_search import member_search_bp
from core.routes.user_collections import user_posts_bp
from core.routes.member_collections import member_posts_bp
from core.routes.cart import cart
from core.routes.member_profiles import member_profile_bp


app = create_app()

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
