from django.urls import path
from order.views import Pay, SaveOrder, Detail

app_name = 'order'

urlpatterns = [
    path('', Pay.as_view(), name='pay'),
    path('save_order/', SaveOrder.as_view(), name='save_order'),
    path('detail/', Detail.as_view(), name='detail'),
]
