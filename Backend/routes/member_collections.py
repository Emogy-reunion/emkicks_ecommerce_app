'''
retrieve sneakers and jerseys for logged in users
'''
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required
from utils.role import role_required
from models import Sneakers, Images, db, Jerseys, JerseyImages
from sqlalchemy.orm import selectinload

member_posts_bp = Blueprint('member_posts_bp', __name__)


@jwt_required()
@member_posts_bp.route('/member_men_sneaker_preview', methods=['GET'])
def member_men_sneakers_preview():
    '''
    retrieves men sneakers previews for logged in users
    '''
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 15, type=int)

    paginated_results = None

    try:
        sneakers = Sneakers.query\
                .filter(Sneakers.category == 'men')\
                .order_by(Sneakers.id.desc())\
                .options(selectinload(Sneaker.images))\
                .all()
        paginated_results = sneakers.paginate(page=page, per_page=per_page)
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500

    if not paginated_results.items:
        return jsonify({'error': 'No sneaker available at at the moment. Stay tuned for new arrivals!'}), 404
    else:
        sneakers = [
                {
                    'name': sneaker.name,
                    'sneaker_id': sneaker.id,
                    'price': sneaker.final_price,
                    'discount': sneaker.discount_rate,
                    'original_price': sneaker.original_price,
                    'status': sneaker.status,
                    'image': sneaker.images[0].filename if sneaker.images else None
                    }
                for sneaker in paginated_results.items
                ]

        response = {
                'sneakers': sneakers,
                'pagination': {
                    'page': paginated_results.page,
                    'per_page': paginated_results.per_page,
                    'pages': paginated_results.pages,
                    'total': paginated_results.total,
                    'next': paginated_results.next_num if paginated_results.has_next else None,
                    'previous': paginated_results.prev_num if paginated_results.has_prev else None
                    }
                }
        return jsonify(response), 200

@jwt_required()
@member_posts_bp.route('/member_women_sneaker_preview', methods=['GET'])
def member_women_sneakers_preview():
    '''
    retrieves women sneaker previews for logged in users
    '''
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 15, type=int)

    paginated_results = None

    try:
        sneakers = Sneakers.query\
                .filter(Sneakers.category == 'women')\
                .order_by(Sneakers.id.desc())\
                .options(selectinload(Sneaker.images))\
                .all()
        paginated_results = sneakers.paginate(page=page, per_page=per_page)
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
    
    if not paginated_results.items:
        return jsonify({"error": 'No sneaker available at the moment. Stay tuned for new arrivals!'}), 404
    else:
        sneakers = [
                {
                    'name': sneaker.name,
                    'sneaker_id': sneaker.id,
                    'price': sneaker.final_price,
                    'discount': sneaker.discount_rate,
                    'original_price': sneaker.original_price,
                    'status': sneaker.status,
                    'image': sneaker.images[0].filename if sneaker.images else None
                    }
                ]
        response = {
                'sneakers': sneakers,
                'pagination': {
                    'page': paginated_results.page,
                    'per_page': paginated_results.per_page,
                    'pages': paginated_results.pages,
                    'total': paginated_results.total,
                    'next': paginated_results.next_num if paginated_results.has_next else None,
                    'previous': paginated_results.prev_num if paginted_results.has_prev else None
                    }
                }
        return jsonify(response), 200

@jwt_required()
@member_posts_bp.route('/member_kids_sneakers_preview', methods=['GET'])
def member_kids_sneakers_preview():
    '''
    retrieves the kids sneakers preview for logged in users
    '''
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 15, type=int)

    paginated_results = None

    try:
        sneakers = Sneaker.query\
                .filter(Sneakers.category == 'kids')\
                .order_by(Sneakers.id.desc())\
                .options(selectinload(Sneakers.images))\
                .all()
        paginated_results = sneakers.paginate(page=page, per_page=per_page)
    except Exception as e:
        return jsonify({"error": 'An unexpected error occured. Please try again!'}), 500

    if not paginated_results.items:
        return jsonify({"error": 'No sneaker available at the momen. Stay tuned for new arrivals!'}), 404
    else:
        sneakers = [
                {
                    'name': sneaker.name,
                    'sneaker_id': sneaker.id,
                    'price': sneaker.final_price,
                    'discount': sneaker.discount_rate,
                    'original_price': sneaker.original_price,
                    'status': sneaker.status,
                    'image': sneaker.images[0].filename if sneaker.images else None
                    }
                for sneaker in paginated_results.items
                ]
        response = {
                'sneakers': sneakers,
                'pagination': {
                    'page': paginated_results.page,
                    'per_page': paginated_results.per_page,
                    'pages': paginated_results.pages,
                    'total': paginated_results.total,
                    'next': paginated_results.next_num if paginated_results.has_next else None,
                    'previous': paginated_results.prev_num if paginated_results.has_prev else None
                    }
                }
        return jsonify(response), 200

@jwt_required()
@member_posts_bp.route('/member_jerseys_preview', methods=['GET'])
def member_jerseys_preview():
    '''
    retrieves the jerseys previews for logged in users
    '''
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 15, type=int)

    paginated_results = None

    try:
        jerseys = Jerseys.query\
                .order_by(Jerseys.id.desc())\
                .options(selectionload(Jerseys.images))\
                .all()
        paginated_results = jerseys.paginate(page=page, per_page=per_page)
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500

    if not paginated_results.items:
        return jsonify({'error': 'No jersey available at the moment. Stay tuned for new arrivals!'}), 404
    else:
        jerseys = [
                {
                    'name': jersey.name,
                    'jersey_id': jersey.id,
                    'price': jersey.final_price,
                    'discount': jersey.discount_rate,
                    'original_price': jersey.original_price,
                    'status': jersey.status,
                    'season': jersey.season,
                    'images': jersey.images[0].filename if jersey.images else None
                    }
                for jersey in paginated_results.items
                ]
        response = {
                'jerseys': jerseys,
                'pagination': {
                    'page': paginated_results.page,
                    'per_page': paginated_results.per_page,
                    'pages': paginated_results.pages,
                    'total': paginated_results.total,
                    'next': paginated_results.next_num if paginated_results.has_next else None,
                    'previous': paginated_results.prev_num if paginated_results.has_prev else None
                    }
                }
        return jsonify(response)

@jwt_required()
@member_posts_bp.route('/member_sneaker_details/<int:sneaker_id>', methods=['GET'])
def member_sneaker_details(sneaker_id):
    '''
    retrieves the sneaker details from the database
    '''
    sneaker = None
    try:
        sneaker = db.session.get(Sneakers, sneaker_id).options(selectinload(Sneakers.images))
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500

    if not sneaker:
        return jsonify({"error": 'Sneaker not found!'}), 404
    else:
        sneaker_details = {
                'name': sneaker.name,
                'sneaker_id': sneaker.id,
                'price': sneaker.final_price,
                'discount': sneaker.discount_rate,
                'original_price': sneaker.original_price,
                'status': sneaker.status,
                'size': sneaker.size,
                'category': sneaker.category,
                'description': sneaker.description,
                'brand': sneaker.brand,
                'status': sneaker.status,
                'images': [image.filename for image in sneaker.images] if sneaker.images else None
                }
        return jsonify(sneaker_details), 200

@jwt_required()
@member_posts_bp.route('/member_jersey_details/<int:jersey_id>', methods=['GET'])
def member_jersey_details(jersey_id):
    '''
    retrieves jersey details for logged in users
    '''
    jersey = None

    try:
        jersey = db.session.get(Jerseys, jersey_id).options(selectionload(Sneakers.images))
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500

    if not jersey:
        return jsonify({"error": 'Jersey not found!'}), 404
    else:
        jersey_details = {
                'name': jersey.name,
                'jersey_id': jersey.id,
                'price': jersey.final_price,
                'discount': jersey.discount_rate,
                'original_price': jersey.original_price,
                'status': jersey.status,
                'season': jersey.season,
                'jersey_type': jersey.jersey_type,
                'size': jersey.size,
                'description': jersey.description,
                'images': [image.filename for image in jersey.images] if jersey.images else None
                }
        return jsonify(jersey_details), 200
