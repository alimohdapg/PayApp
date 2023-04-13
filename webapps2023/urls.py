from django.contrib import admin
from django.urls import include, path
from payapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('register/', include('register.urls')),
    path('payapp/', include('payapp.urls')),
    path('', views.home, name='index')
]
