'''
contains products filtering routes for logged in users
'''
from routes.user_search import find
from models import Sneakers, Images, Jerseys, JerseyImages
from flask import request, jsonify
from sqlalchemy.orm import selectinload
from flask_jwt_extended import jwt_required

@jwt_required()
@find.route('/member_sneaker_search', methods=['GET']\)
def member_sneaker_search():
    '''
    allows user to filter sneakers
    '''
    name = request.args.get('name').lower()
    maximum_price = float(request.args.get('maximum_price'))
    minimum_price = float(request.args.get('mimimum_price'))
    size = int(request.args.get('size'))
    brand = request.args.get('brand').lower()
    category = request.args.get('category').lower()

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 15, type=int)

    sneakers = None

    try:
        sneakers = Sneakers.query.options(selectinload(Sneakers.images))

        if not sneakers:
            return jsonify({"error": 'No sneakers available at athe moment. Stay tuned for new arrivals!'}), 404

        if category:
            sneakers = sneakers.filter(Sneakers.category.ilike('%{category}%'))

        if name:
            sneakers = sneakers.filter(Sneakers.name.ilike(f'%{name}%'))

        if maximum_price is not None:
            if maximum_price <= 0:
                return jsonify({'error': 'Maximum price cannot be less than or equal to 0!'}), 400
            sneakers = sneakers.filter(Sneakers.final_price <= maximum_price)

        if minimum_price is not None:
            if minimum_price < 0:
                return jsonify({'error': 'Minimum price cannot be less than 0'}), 400
            sneakers = sneakers.filter(Sneakers.final_price >= minimum_price)

        if size is not None:
            if size < 35:
                return jsonify({'error': 'Size cannot be less than 35!'}), 400
            sneakers = sneakers.filter(Sneakers.size == size)

        if brand:
            sneakers = sneakers.filter(Sneakers.brand.ilike(f'%{brand}%'))

        paginated_results = sneakers.paginate(page=page, per_page=per_page)

        if not paginated_results.items:
            return jsonify({"error": 'No sneakers match your selected criteria!'}), 404
        else:
            sneakers = [
                    {
                        'name': sneaker.name,
                        'sneaker_id': sneaker.id,
                        'price': sneaker.final_price,
                        'original_price': sneaker.original_price,
                        'discount': sneaker.discount_rate,
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
@find.route('/member_jersey_search', methods['GET'])
def member_jersey_search():
    '''
   allows logged in users to filter jerseys
   '''
   name = request.args.get('name').lower()
   maximum_price = float(request.args.get('maximum_price'))
   minimum_price = float(request.args.get('minimum_price'))
   size = request.args.get('size').lower()
   season = request.args.get('season').lower()
   jersey_type = request.args.get('jersey_type').lower()



