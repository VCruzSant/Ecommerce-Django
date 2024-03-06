def total_cart(cart):
    return sum([i['amount'] for i in cart.values()])
