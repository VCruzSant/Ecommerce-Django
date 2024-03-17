from django.urls import path
from order.views import Pay, SaveOrder, DetailOrder, ListOrders

app_name = 'order'

urlpatterns = [
    path('pagar/<int:pk>', Pay.as_view(), name='pay'),
    path('save_order/', SaveOrder.as_view(), name='save_order'),
    path('detail/<int:pk>', DetailOrder.as_view(), name='detail_order'),
    path('list_order/', ListOrders.as_view(), name='list_order'),
]
