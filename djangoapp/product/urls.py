from django.urls import path
from product.views import (
    ProductList, ProducDetails, AddToCart,
    RemoveFromCart, Cart, Finish,
)

app_name = 'product'

urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('product/<slug>', ProducDetails.as_view(), name='detail'),
    path('addtocart/', AddToCart.as_view(), name='addtocart'),
    path('removefromcart/', RemoveFromCart.as_view(), name='removefromcart'),
    path('cart/', Cart.as_view(), name='cart'),
    path('finish/', Finish.as_view(), name='finish'),
]
