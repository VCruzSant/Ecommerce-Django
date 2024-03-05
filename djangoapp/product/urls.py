from django.urls import path
from product.views import (
    ProductList, ProducDetails, AddToCart,
    RemoveFromCart, Cart, Finish,
)

app_name = 'product_app'

urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('product/<slug:slug>', ProducDetails.as_view(), name='product'),
    path('addtocart/', AddToCart.as_view(), name='addtocart'),
    path('removefromcart/', RemoveFromCart.as_view(), name='removefromcart'),
    path('cart/', Cart.as_view(), name='cart'),
    path('finish/', Finish.as_view(), name='finish'),
]
