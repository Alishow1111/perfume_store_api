# todo/todo/urls.py : Main urls.py
from django.contrib import admin
from django.urls import path, include
from perfume_store_api import urls as perfume_store_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('perfume_store/', include(perfume_store_urls)),
]