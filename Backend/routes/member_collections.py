'''
retrieve sneakers and jerseys for logged in users
'''
from flask import request, jsonify
from routes.user_collections import posts
from flask_jwt_extended import jwt_required
from utils.role import role_required
from models import Sneakers, Images
from sqlalchemy.orm import selectinload

@jwt_required()
@posts.route('/member_men_sneaker_preview', methods=['GET'])
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
                    'discount': sneaker.discount_rate.
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
@post.route('/member_women_sneaker_preview', method=['GET'])
def member_women_sneaker_preview():
    '''
    retrieves sneaker previews for women sneakers
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
