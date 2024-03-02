from django.urls import path
from user_profile.views import Create, Upate, Login, Logout

app_name = 'user_profile'

urlpatterns = [
    path('', Create.as_view(), name='create'),
    path('update/', Upate.as_view(), name='update'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
