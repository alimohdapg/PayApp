from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name="home"),
    path('send_payment', views.send_payment, name="send_payment"),
    path('request_payment', views.request_payment, name="request_payment"),
    path('requests', views.requests, name="requests"),
    path('history', views.history, name="history"),
    path('accounts', views.accounts, name="accounts"),
    path('transactions', views.transactions, name="transactions"),
]
