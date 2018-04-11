from django.urls import path
from django.contrib.auth import views as auth_views
from account import views

app_name = 'account'

urlpatterns = [
    path('',auth_views.LoginView.as_view(template_name="account/login.html"), name='index',),
    path('login', views.login, name='login'),
    path('register', views.UserRegistrationView.as_view(), name='register'),
    path('register-success', views.RegisterSuccessView.as_view(), name='register-success'),
    path('home', views.IndexView.as_view(), name='home'),
    path('token', views.token, name='token'),
]
