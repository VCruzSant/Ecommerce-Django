from django.urls import path
from user_profile.views import RegisterView, UpdateView, LoginView, LogoutView

app_name = 'user_profile'

urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
    path('update/', UpdateView.as_view(), name='update'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
