'''
contain routes that fetch item collections from the database
'''
from flask import Blueprint, request, jsonify
from models import db, Sneakers, Images
from sqlalchemy.orm import selectinload


user_posts_bp = Blueprint('user_posts_bp', __name__)

@user_posts_bp.route('/user_men_sneakers_preview', methods=['GET'])
def user_men_sneakers_preview():
    '''
    retrieve the men's sneakers for preview display
    returns paginated results
    '''
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 15, type=int)

    paginated_results = None

    try:
        sneakers = Sneakers.query \
                .filter(Sneakers.category == 'men') \
                .order_by(Sneakers.id.desc()) \
                .options(selectinload(Sneakers.images)) \
                .all()
        paginated_results = sneakers.paginate(page=page, per_page=per_page)
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500

    if not paginated_results.items:
        return jsonify({'error': 'No sneakers available at the moment. Stay tuned for new arrivals!'}), 404
    else:
        sneakers = [
                {
                    'name': item.name,
                    'sneaker_id': item.id,
                    'status': item.status,
                    'price': item.final_price,
                    'original_price': item.original_price,
                    'discount': item.discount_rate,
                    'image': item.images[0].filename if item.images else None
                    }
                for item in paginated_results.items
                ]

        response = {
                'sneakers': sneakers,
                'pagination': {
                    'page': paginated_results.page,
                    'per_page': paginated_results.per_page,
                    'next': paginated_results.next_num if paginated_results.has_next else None,
                    'previous': paginated_results.prev_num if paginated_results.has_prev else None,
                    'total': paginated_results.total,
                    'pages': paginated_results.pages
                    }
                }
        return jsonify(response), 200


@user_posts_bp.route('/user_women_sneaker_preview', methods=['GET'])
def user_women_sneakers_preview():
    '''
    retrieves the preview for the women's sneakers
    '''
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 15, type=int)

    paginated_results = None

    try:
        sneakers = Sneakers.query \
                .filter(Sneakers.category == 'women') \
                .order_by(Sneakers.id.desc()) \
                .options(selectinload(Sneakers.images)) \
                .all()
        paginated_results = sneakers.paginate_results(page=page, per_page=per_page)
    except Exception as e:
        return jsonify({"error": 'An unexpected error occured. Please try again!'}), 500

    if not paginated_results.items:
        return jsonify({'error': 'No sneakers available at the moment. Stay tuned for new arrivals!'}), 404
    else:
        sneakers = [
                {
                    'name': item.name,
                    'sneaker_id': item.sneaker_id,
                    'status': item.status,
                    'price': item.final_price,
                    'original_price': item.original_price,
                    'discount': item.discount_rate,
                    'image': item.images[0].filename if item.images else None
                    }
                for item in paginated_results.items
                ]
        
        response = {
                'sneakers': sneakers,
                'pagination': {
                    'page': paginated_results.page,
                    'per_page': paginated_results.per_page,
                    'total': paginated_results.total,
                    'pages': paginated_results.pages,
                    'next': paginated_results.next_num if paginated_results.has_next else None,
                    'previous': paginated_results.prev_num if paginated_results.has_prev else None
                    }
                }
        return jsonify(response), 200

@user_posts_bp.route('/user_kids_sneakers_preview', methods=['GET'])
def user_kids_sneakers_preview():
    '''
    retrieves the kids sneakers which will be displayed as preview
    returns the paginated results
    '''
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 15, type=int)

    paginated_results = None

    try:
        sneakers = Sneakers.query \
                .filter(Sneakers.category == 'kids') \
                .order_by(Sneakers.id.desc()) \
                .options(selectinload(Sneakers.images)) \
                .all()
        paginated_results = sneakers.paginate(page=page, per_page=per_page)
    except Exception as e:
        return jsonify({"error": 'An unexpected error occured. Please try again!'}), 500
    

    if not paginated_results.items:
        return jsonify({'error': 'No sneakers available at the moment. Stay tuned for new arrivals!'}), 404
    else:
        sneakers = [
                {
                    'name': item.name,
                    'sneaker_id': item.id,
                    'price': item.final_price,
                    'original_price': item.original_price,
                    'discount': item.discount,
                    'image': item.images[0].filename if item.images else None
                    }
                for item in paginated_results.items
                ]
        response = {
                'sneakers': sneakers,
                'pagination': {
                    'page': paginated_results.page,
                    'per_page': paginated_results.per_page,
                    'pages': paginated_resuls.pages,
                    'total': paginated_results.total,
                    'next': paginated_results.next_num if paginated_results.has_next else None,
                    'previous': paginated_results.prev_num if paginated_results.has_prev else None
                    }
                }
        return jsonify(response), 200

@user_posts_bp.route('/user_jersey_preview', methods=['GET'])
def user_jersey_preview():
    '''
    retrieves the jersey details which will be displayed as a preview
    returns paginated results
    '''
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 15, type=int)

    paginated_results = None
    
    try:
        jerseys = Jerseys.query \
                .options(selectinload(Jerseys.images)) \
                .order_by(Jerseys.id.desc()).all()
        paginated_results = jerseys.paginate_results(page=page, per_page=per_page)
    except Exception as e:
        return jsonify({"error": 'An unexpected error occured. Please try again!'}), 500

    if not paginated_results.items:
        return jsonify({'error': 'No jerseys available at the moment. Stay tuned for new arrivals!'}), 404
    else:
        jerseys = [
                {
                    'name': item.name,
                    'jersey_id': item.id,
                    'price': item.final_price,
                    'original_price': item.original_price,
                    'discount': item.discount_rate,
                    'image': item.images[0].filename if item.images else None
                    }
                ]
        response = {
                'jerseys': jerseys,
                'pagination': {
                    'page': paginated_results.page,
                    'per_page': paginated_results.per_page,
                    'total': paginated_results.total,
                    'pages': paginated_results.pages,
                    'next': paginated_results.next_num if paginated_results.has_next else None,
                    'previous': paginated_results.prev_num if paginated_results.has_prev else None
                    }
                }
        return jsonify(response), 200


@user_posts_bp.route('/user_sneaker_details/<int:sneaker_id>', methods=['GET'])
def user_sneaker_details(sneaker_id):
    '''
    retrieves details about the user sneakers
    '''
    sneaker = None
    try:
        sneaker = db.session.get(Sneakers, sneaker_id).first()
    except Exception as e:
        return jsonify({"error": 'An unexpected error occured. Please try again1'}), 500

    if not sneaker:
        return jsonify({'error': 'Sneaker not found!'}), 404

    details = {
                'name': sneaker.name,
                'sneaker_id': sneaker.id,
                'price': sneaker.final_price,
                'discount_rate': sneaker.discount_rate,
                'original_price': sneaker.original_price,
                'size': sneaker.size,
                'status': sneaker.status,
                'description': sneaker.description,
                'category': sneaker.category,
                'brand': sneaker.brand,
                'posted_at': sneaker.posted_at,
                'images': [image.filename for image in sneaker.images] if sneaker.images else None
                }
    return jsonify({'details': details}), 200

@user_posts_bp.route('/user_jersey_details/<int:jersery_id>', methods=['GET'])
def user_jersey_details(jersey_id):
    '''
    retrieve details about a specific jersey
    '''
    jersey = None

    try:
        jersey = db.session.get(Jerseys, jersey_id).first()
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500

    if not jersey:
        return jsonify({'error': 'Jersey not found!'}), 404

    details = {
            'jersey_id': jersey.id,
            'name': jersey.name,
            'jersey_type': jersey.jersey_type,
            'price': jersey.final_price,
            'discount_rate': jersey.discount_rate,
            'original_price': jersey.original_price,
            'size': jersey.size,
            'status': jersey.status,
            'season': jersey.season,
            'description': jersey.description,
            'posted_at': jersey.posted_at,
            'images': [image.filename for image in jersey.images] if jersey.images else None
            }
    return jsonify({'details': details}), 200

