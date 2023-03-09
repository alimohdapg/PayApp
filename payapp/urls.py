from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name="home"),
    path('send_payment', views.send_payment, name="send_payment"),
    path('request_payment', views.request_payment, name="request_payment"),
    path('requests', views.requests, name="requests"),
    path('history', views.history, name="history"),
    path('delete_request', views.delete_request, name="delete_request"),
    path('accept_request', views.accept_request, name="accept_request"),
    path('accounts', views.accounts, name="accounts"),
    path('transactions', views.transactions, name="transactions"),
]
