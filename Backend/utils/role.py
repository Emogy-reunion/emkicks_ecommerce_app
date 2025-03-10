'''
checks the user role
'''
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from model import Users


def role_required(role):

    def decorator(func):
        '''
        func: the decorated route's function
        '''
        @wraps(func) #wraps the function to preserve it's documentation
        def wrapper(*args, **kwargs):
            '''
            extends the functionality of the decorated function
            '''
            user_id = get_jwt_identity()
            current_user = db.session.get(Users, user_id)
            if current_user.role != role:
                return jsonify({'error': "Unauthorized access!"}), 403

            return func(*args, **kwargs) #calls the decorated function
        return wrapper
    return decorator

