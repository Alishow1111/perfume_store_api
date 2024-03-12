from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Category, Product, Order, OrderItem
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, OrderItemSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import authentication



class Login(APIView):
    
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response({"detail": "Not Found."}, status=status.HTTP_404_NOT_FOUND)
        
        token, created = Token.objects.get_or_create(user=user)
        
        # Pass the user instance and data to the serializer
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            return Response({"token": token.key, "user": serializer.data})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class Signup(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({"token": token.key, "user": serializer.data})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class Test_Token(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication ]

    def get(self, request, *args, **kwargs):
        return Response("passed!")
        
        


# Create your views here.
class CategoryListView(APIView):

    #retrieve all categories
    def get(self, request, *args, **kwargs):
        categories = Category.objects
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #create a new category
    def post(self, request, *args, **kwargs):
        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description')
        }
        serializer = CategorySerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductListView(APIView):

    #retrieve all products in the store
    def get(self, request, *args, **kwargs):
        products = Product.objects
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #create a new product in the store
    def post(self, request, *args, **kwargs):

        data = {
            'category': request.data.get('category'),
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            'price': request.data.get('price'),
            'stock': request.data.get('stock'),
            'image': request.data.get('image'),
        }

        serializer = ProductSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OrderListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication ]


    #retrieve all orders for admin
    def get(self, request, *args, **kwargs):
        orders = Order.objects
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #order created for user signed in
    def post(self, request, *args, **kwargs):
        data = {
            'user': request.user.id,
            'paid': request.data.get('paid')
        }
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication ]


    def get_objects(self, order_id):
        try:
            return OrderItem.objects.get(id=order_id)
        except OrderItem.DoesNotExist:
            return None

    #retrieve all order items with specified order_id
    def get(self, request, order_id, *args, **kwargs):
        order_item_instance = self.get_objects(order_id)
        if not order_item_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = OrderItemSerializer(order_item_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, order_id, *args, **kwargs):
        data = {
            'order': order_id,
            'product': request.data.get('product'),
            'price': request.data.get('price'),
            'quantity': request.data.get('quantity')
        }

        serializer = OrderItemSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)











