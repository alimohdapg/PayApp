from django.urls import path
from . import views

urlpatterns = [
    path('register_user', views.register_user, name="register_user"),
    path('register_admin', views.register_admin, name="register_admin"),
    path('login_user', views.login_user, name="login_user"),
    path('logout_user', views.logout_user, name="logout_user")
]
