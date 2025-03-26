'''
contains routes that allow the users to filter products
'''
from flask import Blueprint, jsonify, request
from models import Sneakers, Images
from sqlalchemy.orm import selectinload

find = Blueprint('find', __name__)

@find.route('/user_sneakers_search', methods=['GET'])
def user_sneakers_search():
    '''
    allows user to filter sneakers
    '''
    name = request.args.get('name').lower()
    minimum_price = request.args.get('minimum_price', type=float)
    maximum_price = request.args.get('maximum_price', type=float)
    category = request.args.get('category').lower()
    size = request.args.get('size', type=int)
    brand = request.args.get('brand').lower()
    page = request.args.get('page', type=int)
    per_page = request.args.get('per_page', type=int)

    sneakers = None

    try:
        sneakers = Sneakers.query.options(selectionload(Sneakers.images))

        if not sneakers:
            return jsonify({'error': 'No sneakers available at the moment. Stay tuned for new arrivals!'}), 404

        if name:
            sneakers = sneakers.filter(Sneakers.name.ilike(f'%{name}%'))

        if minimum_price is not None:
            if minimum_price < 0:
                return jsonify({'error': 'Minimum price cannot be less than zero!'}), 400
            sneakers = sneakers.filter(Sneakers.minimum_price >= minimum_price)

        if maximum_price is not None:
            if maximum_price <= 0:
                return jsonify({'error': 'Maximum price cannot be less than or equal to zero'}), 400
            sneakers = sneakers.query.filter(Sneakers.maximum_price <= maximum_price)

        if category:
            sneakers = sneakers.query.filter(Sneakers.category.ilike(f'%{category}%'))

        if size is not None:
            if size <= 0:
                return jsonify({'error': 'Size cannot be less than or equal to zero'}), 400
            sneakers = sneakers.query.filter(Sneakers.size == size)

        if brand:
            sneakers = sneakers.query.filter(Sneakers.brand.ilike(f'%{brand}%'))

        paginated_results = sneakers.paginate(page=page, per_page=per_page)

        if not paginated_results.items:
            return jsonify({'error': 'No sneakers match your selected criteria!'}), 404
        else:
            sneaker_results = [
                    {
                        'name': sneaker.name,
                        'sneaker_id': sneaker.id,
                        'price': sneaker.final_price,
                        'original_price': sneaker.original_price,
                        'discount_rate': sneaker.discount_rate,
                        'status': sneaker.status,
                        'image': image.filename if sneaker.images[0].filename else None
                        }
                    for sneaker in paginated_results.items
                    ]
            response = {
                    'results': sneaker_results,
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
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again'}), 500
