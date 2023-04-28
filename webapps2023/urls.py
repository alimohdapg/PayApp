from django.contrib import admin
from django.urls import include, path
from payapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('register/', include('register.urls')),
    path('payapp/', include('payapp.urls')),
    path('conversion/<currency1>/<currency2>/<amount_of_currency1>', views.Conversion.as_view(), name="conversion"),
    path('', views.home, name='index')
]
