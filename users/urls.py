from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, VerifyEmailView, GenerateAndSendPasswordView, UserUpdateView

app_name=UsersConfig.name

urlpatterns=[
    path('',LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('verify_email/', VerifyEmailView.as_view(), name='verify_email'),
    path('generate_and_send_password/', GenerateAndSendPasswordView.as_view(), name='generate_and_send_password'),

]