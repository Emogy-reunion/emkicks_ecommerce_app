'''
saves uploads to the database
'''
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from utils.role import role_required
import os
from model import Users, Sneakers, Images, db
from check_file_extension import allowed_extension
from werkzeug.utils import secure_filename

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

    uploads = []

    for file in request.files:
        '''
        iterate through the files object
        save the image filenames in the images table
        '''
        if file and allowed_extension(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            sneaker_image = Images(sneaker_id=new_sneaker.id, filename=filename)
            uploads.append(filename)
            db.session.add(sneaker_image)
        else:
            return jsonify({'error': 'Invalid file format or file missing. Please try again!'}), 400
    db.session.commit()

    if uploads:
        return jsonify({'success': 'Post submitted successfully!'}), 201
    else:
        return jsonify({'error': 'Post submission failed. Please try again!'}), 400
