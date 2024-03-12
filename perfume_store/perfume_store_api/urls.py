# todo/todo/urls.py : Main urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.Login.as_view()),
    path('signup', views.Signup.as_view()),
    path('test_token', views.Test_Token.as_view()),
    path('categories', views.CategoryListView.as_view()),
    path('products', views.ProductListView.as_view()),
    path('orders', views.OrderListView.as_view()),
    path('orderItems/<int:order_id>/', views.OrderItemView.as_view())
    
]