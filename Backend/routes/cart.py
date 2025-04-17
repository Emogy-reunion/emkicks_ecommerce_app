'''
contains routes that perform CRUD operations for the cart
'''
from flask import Blueprint, jsonify, request
from forms import SizeQuantityForm
from models import Sneakers, Jerseys, Images, Cart, CartItems, db
from flask_jwt_extended import jwt_required


cart = Blueprint('cart', __name__)

@cart.route('/add_to_cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    '''
    adds items to the cart
    '''
    form = SizeQuantityForm(data=request.get_json())

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
            
            if sneaker:
                price = sneaker.final_price
            else:
                return jsonify({"error": 'Item not found!'}), 404
        elif product_type == 'jersey':
            jersey = Jerseys.query.filter_by(id=product_id).first()

            if jersey:
                price = jersey.final_price
            else:
                return jsonify({"error": 'Item not found!'}), 404
        else:
            return jsonify('error': 'Invalid product type!'}), 400

        subtotal = quantity * price

        cart = Cart.query.filter_by(user_id=user_id).options(selectinload(Cart.items)).first()

        if not cart:
            '''
            if the cart doesn't exist create it
            '''
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.commit()

        if cart.items:
            for item in cart.items:
                if item.product_id == product_id and item.size == size:
                    item.quantity += 1
                    item.subtotal = item.price * item.quantity
                    db.session.commit()
                    found = True
                    return jsonify({'success': 'Item added to cart!'}), 201
        
        subtotal = quantity * price
        item = CartItem(cart_id=cart.id, product_id=product_id, price=price,
                        product_type=product_type, quantity=quantity,
                        size=size, subtotal=subtotal)
        db.session.add(item)
        db.session.commit()
        return jsonify({'success': 'Item added to cart!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500


@cart.route('/clear_cart', methods=['DELETE'])
@jwt_required()
def clear_cart():
    '''
    clears all items from the cart
    '''
    try:
        user_id = get_jwt_identity()

        cart = Cart.query.filter_by(user_id=user_id).first()

        if not cart:
            return jsonify({'error': 'Cart not found!'}), 404

        CartItems.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()
        return jsonify({'success': 'Cart cleared successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
