from django.urls import path
from order.views import Pay, CloseOrder, Detail

app_name = 'order'

urlpatterns = [
    path('', Pay.as_view(), name='pay'),
    path('close_order/', CloseOrder.as_view(), name='close_order'),
    path('detail/', Detail.as_view(), name='detail'),
]
