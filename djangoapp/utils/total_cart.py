def total_cart(cart):
    return sum(
        [
            i.get('quantitative_price_promotional')
            if i.get('quantitative_price_promotional')
            else i.get('quantitative_price')
            for i
            in cart.values()
        ]
    )
