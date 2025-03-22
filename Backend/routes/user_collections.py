'''
contain routes that fetch item collections from the database
'''
from flask import Blueprint, request, jsonify
from model import db, Sneakers, Images
from sqlalchemy.orm import selectinload


posts = Blueprint('posts', __name__)

@posts.route('/men_sneakers_preview', methods=['GET'])
def men_sneakers_preview():
    '''
    retrieve the men's sneakers for preview display
    returns paginated results
    '''
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 15, type=int)

    sneakers = Sneakers.query \
            .filter(Sneakers.category == 'men') \
            .order_by(Sneakers.id.desc()) \
            .options(selectinload(Sneakers.images)) \
            .all()
    paginated_results = sneakers.paginate(page=page, per_page=per_page)

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


@posts.route('/women_sneaker_preview', methods=['GET'])
def women_sneakers_preview():
    '''
    retrieves the preview for the women's sneakers
    '''
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 15, type=int)

    sneakers = Sneakers.query \
            .filter(Sneakers.category == 'women') \
            .order_by(Sneakers.id.desc()) \
            .options(selectinload(Sneakers.images)) \
            .all()
    paginated_results = sneakers.paginate_results(page=page, per_page=per_page)

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

@posts.routes('/kids_sneakers_preview', methods=['GET'])
def kids_sneakers_preview():
    '''
    retrieves the kids sneakers which will be displayed as preview
    returns the paginated results
    '''
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 15, type=int)

    sneakers = Sneakers.query \
            .filter(Sneakers.category == 'kids') \
            .order_by(Sneakers.id.desc()) \
            .options(selectinload(Sneakers.images)) \
            .all()
    paginated_results = sneakers.paginate(page=page, per_page=per_page)

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

@posts.route('/jersey_preview', methods=['GET'])
def jersey_preview():
    '''
    retrieves the jersey details which will be displayed as a preview
    returns paginated results
    '''
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 15, type=int)

    jerseys = Jerseys.query \
            .options(selectinload(Jerseys.images)) \
            .order_by(Jerseys.id.desc()).all()
    paginated_results = jerseys.paginate_results(page=page, per_page=per_page)

    if not paginated_results.items:
        return jsonify({'error': 'No jerseys available at the moment. Stay tuned for new arrivals!'}), 404
    else:
        jerseys = [
                {
                    'name': item.name,
                    'jersey_id': item.id,
                    'price': item.fianal_price,
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
                    'next': paginated_results.next_num if paginated_results.has_next,
                    'previous': paginated_results.prev_num if paginated_results.has_prev
                    }
                }
        return jsonify(response), 200

