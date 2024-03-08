from django.template import Library
from utils import total_cart_quantity, total_cart

register = Library()


@register.filter
def cart_total_qntt(cart):
    return total_cart_quantity.total_cart_quantity(cart)


@register.filter
def cart_total(cart):
    return total_cart.total_cart(cart)
