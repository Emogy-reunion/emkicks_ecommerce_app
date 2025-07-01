'''
saves uploads to the database
'''
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from core.utils.role import role_required
from core.utils.discount import calculate_discount
import os
from core.models import Users, Sneakers, Images, Jerseys, JerseyImages
from core import db
from core.utils.check_file_extension import allowed_extension
from werkzeug.utils import secure_filename
from forms import SneakerUploadForm, JerseyUploadForm

post = Blueprint('post', __name__)

@post.route('/sneaker_upload', methods=['POST'])
@jwt_required()
@role_required('admin')
def sneaker_upload():
    '''
    allows admins to  upload sneaker details and  photos
    '''
    if not request.files:
        return jsonify({'error': 'No file uploaded. Please select one or more files and try again!'}), 400

    form = SneakerUploadForm(data=request.form)

    if form.validate():
        original_price = form.original_price.data
        discount_rate = form.discount_rate.data
        size = form.size.data.lower()
        description = form.description.data
        status = form.status.data
        category = form.category.data
        brand = form.brand.data
        season = form.season.data

        final_price = original_price
        upload = []

        if discount_rate > 0:
            final_price = calculate_discount(discount_rate=discount_rate, original_price=original_price)

        try:
            user_id = get_jwt_identity()
            new_sneaker = Sneakers(name=name, original_price=original_price, size=size, brand=brand,
                                   user_id=user_id, discount_rate=discount_rate, final_price=final_price,
                                   description=description, status=status, category=category)
            db.session.add(new_sneaker)
            db.session.flush()

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
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500

        if uploads:
            return jsonify({'success': 'Post submitted successfully!'}), 201
        else:
            return jsonify({'error': 'Post submission failed. Please try again!'}), 400
    else:
        return jsonify({'error': form.errors}), 400


@post.route('/jersey_upload', methods=['POST'])
@jwt_required()
@role_required('admin')
def jersey_upload():
    '''
    allows the admin to upload jerseys and their details
    '''
    if not request.files:
        return jsonify({'error': 'No file uploaded. Please select one or more files and try again!'}), 400

    form = JerseyUploadForm(data=request.form)

    if form.validate():
        name = form.name.data
        jersey_type = form.jersey_type.data
        original_price = form.original_price.data
        discount_rate = form.discount_rate.data
        status = form.status.data
        size = form.size.data
        season = form.season.data
        description = form.description.data

        final_price = original_price
        uploads = []

        try:
            user_id = get_jwt_identity()

            if discount_rate > 0:
                final_price = calculate_discount(discount_rate=discount_rate, original_price=original_price)

            new_jersey = Jerseys(name=name, jersey_type=jersey_type, original_price=original_price, discount_rate=discount_rate,
                                 user_id=user_id, final_price=final_price, status=status, size=size, season=season, description=description)
            db.session.add(new_jersey)
            db.session.flush()

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
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                new_file = JerseyImages(jersey_id=new_jersey.id, filename=filename)
                db.session.add(new_file)
                upload.append(new_file)
            else:
                return jsonify({'error': 'Invalid email format or file missing. Please try again!'}), 400
           db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
    
        if uploads:
            return jsonify({'success': 'Post submitted successfully!'}), 201
        else:
            return jsonify({'error': 'Post submission failed. Please try again!'}), 400
    else:
        return jsonify({'errors': form.errors}), 400
