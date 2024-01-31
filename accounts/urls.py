from django.urls import path
from .views import auth

app_name = "accounts" 

urlpatterns = [
    path('signup/', auth.UserSignUp.as_view(), name='user_signup'),
    path('login/', auth.LoginView.as_view(), name='login_user'),
]
