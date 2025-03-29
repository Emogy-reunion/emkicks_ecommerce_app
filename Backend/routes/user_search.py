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
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 15, type=int)

    sneakers = None

    try:
        sneakers = Sneakers.query.options(selectionload(Sneakers.images))

        if category:
            sneakers = sneakers.filter(Sneakers.category.ilike(f'%{name}%'))

        if not sneakers:
            return jsonify({'error': 'No sneakers available at the moment. Stay tuned for new arrivals!'}), 404

        if name:
            sneakers = sneakers.filter(Sneakers.name.ilike(f'%{name}%'))

        if minimum_price is not None:
            if minimum_price < 0:
                return jsonify({'error': 'Minimum price cannot be less than zero!'}), 400
            sneakers = sneakers.filter(Sneakers.final_price >= minimum_price)

        if maximum_price is not None:
            if maximum_price <= 0:
                return jsonify({'error': 'Maximum price cannot be less than or equal to zero'}), 400
            sneakers = sneakers.query.filter(Sneakers.final_price <= maximum_price)

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
                        'image': sneaker.images[0].filename if sneaker.images else None
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

@find.route('/user_jerseys_search', methods=['GET'])
def user_jerseys_search():
    '''
    allows users to filter jerseys according to certain criteria
    '''
    name = request.args.get('name').lower()
    minimum_price = request.args.get('minimum_price', type=float)
    maximum_price = request.args.get('maximum_price', type=float)
    size = request.args.get('size').lower()
    season = request.args.get('season').lower()
    jersey_type = request.args.get('jersey_type').lower()

    page = request.args.get('page', 1, type=int)
    per_page = reqeust.args.get('per_page', 15, type=int)

    jerseys = None

    try:
        jerseys = Jerseys.query.options(selectinload(Sneakers.images))

        if jerseys:

            if name:
                jerseys = jerseys.filter(Jerseys.name.ilike(f'%{name}%'))

            if minimum_price is not None:
                if minimum_price < 0:
                    return jsonify({'error': 'Minimum price cannot be less than 0!'}), 400
                jerseys = jerseys.filter(Jerseys.final_price >= minimum_price)

            if maximum_price is not None:
                if maximum_price <= 0:
                    return jsonify({'error': 'Maximum price cannot be less than or equal to zero!'}), 400
                jerseys = jerseys.filter(Jerseys.final_price <= maximum_price)

            if season:
                jerseys = jerseys.filter(Jerseys.season.ilike(f'%{season}%'))

            if size:
                jerseys = jerseys.filter(Jerseys.size.ilike(f'%{size}%'))

            if jersey_type:
                jerseys = jerseys.filter(Jerseys.jersey_type.ilike(f'%{jersey_type}%'))

            paginated_results = jerseys.paginate(page=page, per_page=per_page)

            if not paginated_results.items:
                return jsonify({'error': 'No jerseys match your selected criteria!'}), 404
            else:

                jersey_results = [
                        {
                            'name': jersey.name,
                            'jersey_id': jersey.id,
                            'price': jersey.original_price,
                            'original_price': jersey.final_price,
                            'discount_rate': jersey.discount_rate,
                            'status': jersey.status,
                            'image': jersey.images[0].filename if jersey.images else None
                            }
                        for jersey in paginated_results.items
                        ]
                response = {
                        'results': jersey_results,
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
        else:
            return jsonify({'error': 'No sneakers available at the moment. Stay tuned for new arrivals!'}), 404
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
