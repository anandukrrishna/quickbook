from django.urls import path
from .views import *


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('web-login/', web_login, name='web_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('web-logout/', web_logout, name='web_logout'),
]