'''
saves uploads to the database
'''
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from utils.role import role_required
from model import Users, Sneakers, Images, db

post = Blueprint('post', __name__)

@jwt_required()
@role_required('admin')
@post.route('/upload', methods=['POST'])
def upload():
    '''
    allows admins to  upload photos
    '''
    if not request.files:
        return jsonify({'error': 'No file uploaded. Please select one or more files and try again!'}), 400

    data = request.json
    name = data['name']
    price = data['price']
    size = data['size']
    description = data['description']
    status = data['status']
    category = data['category']

    new_sneaker = Sneakers(name=name, price=price, size=size,
                               description=description, status=status, category=category)
    try:
        db.session.add(new_sneaker)
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
    db.session.commit()

    for file in request.files:
        '''
        iterate through the files object
        save the image filenames in the images table
        '''
        if file and 
