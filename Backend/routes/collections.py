'''
contain routes that fetch item collections from the database
'''
from flask import Blueprint
from model import db, Sneakers, Images
from sqlalchemy.orm import selectinload


posts = Blueprint('posts', __name__)

@posts.route('/men_sneakers', methods=['GET'])
def men_sneakers_preview():
    '''
    retrieve the men's sneakers preview
    '''
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 14, type=int)

    sneakers = Users.query.filter_by(category == 'men').order_by(Sneak ers.id.desc()).all()
    paginated_results = sneakers.paginate(page=page, per_page=per_page)

    sneakers = []
    if not paginated_results.items:
        return jsonify({'error': 'Sneakers not found!'})
    else:
        for item in paginated_results.items:
            sneaker.append({
                'name': item.name,
                'price': item.final_price,
                'original_price': item.original_price,
                'discount': item.discount_rate
                'images': [image.filename for image in item.images[0]] if images else None
                })
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
        return jsonify(response)

