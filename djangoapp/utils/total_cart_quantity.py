def total_cart_quantity(cart):
    return sum([i['amount'] for i in cart.values()])
