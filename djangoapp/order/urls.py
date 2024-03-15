from django.urls import path
from order.views import Pay, SaveOrder, Detail, ListOrders

app_name = 'order'

urlpatterns = [
    path('pagar/<int:pk>', Pay.as_view(), name='pay'),
    path('save_order/', SaveOrder.as_view(), name='save_order'),
    path('detail/', Detail.as_view(), name='detail'),
    path('list_order/', ListOrders.as_view(), name='list_order'),
]
