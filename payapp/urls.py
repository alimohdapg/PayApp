from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('convert-currency/<currency1>/<currency2>/<amount>', views.ConvertCurrency.as_view(), name="convert-currency"),
    path('home', views.home, name="home"),
    path('send_payment', views.send_payment, name="send_payment"),
    path('request_payment', views.request_payment, name="request_payment"),
    path('requests', views.requests, name="requests"),
    path('delete_request', views.delete_request, name="delete_request"),
    path('accept_request', views.accept_request, name="accept_request"),
    path('history', views.history, name="history"),
    path('accounts', views.accounts, name="accounts"),
    path('transactions', views.transactions, name="transactions"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
