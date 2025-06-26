'''
logic to calculate the discount
'''
def calculate_discount(original_price, discount_rate):
    '''
    finds the final price after discount
    original_price: price before discount
    discount_rate: the discount
    returns the price after discount as a float
    '''
    discount_amount = (discount_rate / 100) * original_price
    final_price = original_price - discount_amount
    return round(final_price, 2)
