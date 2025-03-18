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

    results = []
    for item in paginated_results.items:
        item

