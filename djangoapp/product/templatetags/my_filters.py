from django.template import Library
from utils import total_cart_quantity

register = Library()


@register.filter
def cart_total(cart):
    return total_cart_quantity.total_cart_quantity(cart)
