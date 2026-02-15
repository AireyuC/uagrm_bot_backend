from django.urls import path
from .api.views import LoginView, LogoutView, UserView, UserCreateView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserView.as_view(), name='user_detail'),
    path('register/', UserCreateView.as_view(), name='user_create'),
]
