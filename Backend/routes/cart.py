'''
contains routes that perform CRUD operations for the cart
'''
from flask import Blueprint, jsonify, request
from forms import SizeQuantityForm


cart = Blueprint('cart', __name__)

@cart.route('/add_to_cart', methods=['POST'])
def add_to_cart(product_id):
    '''
    adds items to the cart
    '''
    form = SizeQuantityForm(request.get_json)

    if not form.validate():
        return jsonify({'error': form.errors}), 400

    product_id = form.product_id.data
    product_type = form.product_type.data
    quantity = form.quantity.data
    size = form.size.data
    price = None
    subtotal = None

    try:
        user_id = get_jwt_identity()
        if product_type == 'sneaker':
            sneaker = Sneakers.query.filter_by(id=product_id).first()
            price = sneaker.final_price
        elif product_type == 'jersey':
            jersey = Jerseys.query.filter-by(id=product_id).first()
            price = jersey.final_price
        else:
            return jsonify('error': 'Invalid product type!'}), 400

        subtotal = quantity * price

        cart = Cart.query.filter_by(user_id=user_id).options(selectinload(Cart.items)).first()

        if not cart:
            '''
            if the cart doesn't exist create it
            '''
            cart = Cart(user_id=user)
            db.session.add(cart)
            db.session.commit()

        if cart.items:
            for item in cart.items:
                if item.product_id == product_id and item.size == size:
                    item.quantity += 1
                    item.subtotal = item.price * item.quantity
                    db.session.commit()
                    return jsonify({'Success': 'Item added successfully'}), 201


        
