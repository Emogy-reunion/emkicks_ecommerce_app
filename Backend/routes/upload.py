'''
saves uploads to the database
'''
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from utils.role import role_required
from utils.discount import calculate_discount
import os
from models import Users, Sneakers, Images, db, Jerseys, JerseyImages
from utils.check_file_extension import allowed_extension
from werkzeug.utils import secure_filename

post = Blueprint('post', __name__)

@jwt_required()
@role_required('admin')
@post.route('/sneaker_upload', methods=['POST'])
def sneaker_upload():
    '''
    allows admins to  upload sneaker details and  photos
    '''
    if not request.files:
        return jsonify({'error': 'No file uploaded. Please select one or more files and try again!'}), 400

    data = request.json
    name = data['name'].lower()
    original_price = float(data['original_price'])
    discount_rate = int(data['discount_rate'])
    size = int(data['size'])
    description = data['description']
    status = data['status'].lower()
    category = data['category'].lower()
    final_price = original_price

    if discount_rate > 0:
        final_price = calculate_discount(discount_rate=discount_rate, original_price=original_price)

    new_sneaker = Sneakers(name=name, original_price=original_price, size=size, 
                           discount_rate=discount_rate, final_price=final_price,
                           description=description, status=status, category=category)
    try:
        db.session.add(new_sneaker)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500

    uploads = []

    for file in request.files:
        '''
        iterate through the files object
        save the image filenames in the images table
        '''
        if file and allowed_extension(file.filename):
            try:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                sneaker_image = Images(sneaker_id=new_sneaker.id, filename=filename)
                uploads.append(filename)
                db.session.add(sneaker_image)
            except Exception as e:
                db.session.rollba()
                return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
        else:
            return jsonify({'error': 'Invalid file format or file missing. Please try again!'}), 400
    db.session.commit()

    if uploads:
        return jsonify({'success': 'Post submitted successfully!'}), 201
    else:
        return jsonify({'error': 'Post submission failed. Please try again!'}), 400

@jwt_required()
@role_required('admin')
@post.route('/jersey_upload', methods=['POST'])
def jersey_upload():
    '''
    allows the admin to upload jerseys and their details
    '''
    if not request.files:
        return jsonify({'error': 'No file uploaded. Please select one or more files and try again!'}), 400

    data = request.json
    name = data['name'].lower()
    jersey_type = data['jersey_type'].lower()
    original_price = float(data['original_price'])
    discount_rate = int(data['discount_rate'])
    status = data['status'].lower()
    size = data['size'].lower()
    season = data['season']
    description = data['description']
    final_price = original_price

    if discount_rate > 0:
        final_price = calculate_discount(discount_rate=discount_rate, original_price=original_price)


    new_jersey = Jerseys(name=name, jersey_type=jersey_type, original_price=original_price, discount_rate=discount_rate,
                         final_price=final_price, status=status, size=size, season=season, description=description)

    try:
        db.session.add(new_jersey)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500

    uploads = []

    for file in request.files:
        '''
        iterates through the file obeject
        '''
        if file and allowed_extension(file.filename):
            '''
            checks if the file exists and has a valid filename
            if the checks pass, 
                it secures the filename
                saves the image in the upload folder
                saves the filename in the database
            '''
            try:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                new_file = JerseyImages(jersey_id=new_jersey.id, filename=filename)
                db.session.add(new_file)
                upload.append(new_file)
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
        else:
            return jsonify({'error': 'Invalid email format or file missing. Please try again!'}), 400
    db.session.commit()

    if uploads:
        return jsonify({'success': 'Post submitted successfully!'}), 201
    else:
        return jsonify({'error': 'Post submission failed. Please try again!'}), 400
