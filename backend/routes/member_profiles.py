from flask import Blueprint
from flask_jwt_extended import jwt_required
from models import Users


member_profile_bp = Blueprint('member_profile_bp', __name__)

@member_profile_bp.route('/member_profile', methods=['GET'])
@jwt_required()
def member_profile():
    '''
    retrieves the logged in users profile
    '''
    try:
        user_id = get_jwt_identity()

        user = db.session.get(Users, user_id)

        if not user:
            return jsonify({'error': 'User not found!'}), 404

        profile = {
                'firstname': user.firstname,
                'lastname': user.lastname,
                'email': user.email,
                'phone': user.phone,
                'username': user.username,
                'joined': user.created_at.strftime('%d %B %Y')
                }
        return jsonify(profile), 200


