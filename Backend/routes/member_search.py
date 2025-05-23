'''
contains products filtering routes for logged in users
'''
from models import Sneakers, Images, Jerseys, JerseyImages
from flask import request, jsonify, Blueprint
from sqlalchemy.orm import selectinload
from flask_jwt_extended import jwt_required
from forms import SneakerSearchForm, JerseySearchForm


member_search_bp = Blueprint('member_search_bp', __name__)

@member_search_bp.route('/member_sneaker_search', methods=['GET'])
@jwt_required()
def member_sneaker_search():
    '''
    allows user to filter sneakers
    '''
    form = SneakerSearchForm(data=request.get_json())

    if not form.validate():
        return jsonify({'error': form.errors}), 400
    
    name = form.name.data.lower()
    minimum_price = form.minimum_price.data
    maximum_price = form.maximum_price.data
    category = form.category.data.lower()
    size = form.size.data
    brand = form.brand.data.lower()

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

    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500


@member_search_bp.route('/member_jersey_search', methods=['GET'])
@jwt_required()
def member_jersey_search():
    '''
    allows logged in users to filter jerseys
    '''

    form = JerseySearchForm(data=request.get_json())

    if not form.validate():
        return jsonify({"error": form.errors}), 400

    name = form.name.data.lower()
    minimum_price = form.minimum_price.data
    maximum_price = form.maximum_price.data
    size = form.size.data.lower()
    season = form.season.lower()
    jersey_type = form.jersey_type.lower()

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 15, type=int)

    try:
        jerseys = Jerseys.query.options(selectinload(Jerseys.images))

        if not jerseys:
            return jsonify({'error': 'No jerseys available at the moment. Stay tuned for new arrivals!'}), 404

        if name:
            jerseys = jerseys.filter(Jerseys.name.ilike(f'%{name}%'))

        if maximum_price is not None:
            if maximum_price <= 0:
                return jsonify({"error": 'Maximum price cannot be less than or equal to zero!'}), 400
            jerseys = jerseys.filter(Jerseys.final_price <= maximum_price)

        if minimum_price is not None:
            if minimum_price < 0:
                return jsonify({"error": 'Minimum price cannot be less than 0!'}), 400
            jerseys = jerseys.filter(Jerseys.final_price >= minimum_price)

        if size:
            jerseys = jerseys.filter(Jerseys.size.ilike(f'%{size}%'))

        if season:
            jerseys = jerseys.filter(Jerseys.season.ilike(f'%{season}%'))

        if jersey_type:
            jerseys = jerseys.filter(Jerseys.jersey_type.ilike(f'%{jersey_type}%'))

        paginated_results = jerseys.paginate(page=page, per_page=per_page)

        if not paginated_results.items:
            return jsonify({'error': 'No jerseys match your selected criteria!'}), 404
        else:
            jerseys = [
                    {
                        'name': jersey.name,
                        'jersey_id': jersey.id,
                        'price': jersey.final_price,
                        'discount': jersey.discount_rate,
                        'original_price': jersey.original_price,
                        'status': jersey.status,
                        'image': jersey.images[0].filename if jersey.images else None
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
            return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
