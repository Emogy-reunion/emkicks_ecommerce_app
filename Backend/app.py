'''
initializes the libraries
creates initial admins
runs the application
'''
from create_app import create_app
from routes.authentication import auth
from flask_jwt_extended import JWTManager


app = create_app()
jwt = JWTManager(app)

app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(debug=True)
