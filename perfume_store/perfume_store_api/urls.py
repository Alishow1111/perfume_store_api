# todo/todo/urls.py : Main urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('categories', views.CategoryListView.as_view()),
    path('products', views.ProductListView.as_view()),
    path('orders', views.OrderListView.as_view()),
    path('orderItems/<int:order_id>/', views.OrderItemView.as_view())
    
]