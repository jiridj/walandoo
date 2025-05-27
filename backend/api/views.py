from django.shortcuts import render
from rest_framework import generics
from .models import Product, Stock, Customer, ShoppingCart, Order, Shipment
from .serializers import ProductSerializer, StockSerializer, CustomerSerializer, ShoppingCartSerializer, OrderSerializer, ShipmentSerializer
from django.http import FileResponse
import os
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsSelf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer, UserProfileSerializer

# Create your views here.

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class StockListView(generics.ListAPIView):
    queryset = Stock.objects.select_related('product').all()
    serializer_class = StockSerializer

class StockDetailView(generics.RetrieveAPIView):
    queryset = Stock.objects.select_related('product').all()
    serializer_class = StockSerializer
    lookup_field = 'product_id'

class CustomerListView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsSelf]

class ShoppingCartListView(generics.ListCreateAPIView):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated]

class ShoppingCartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated]

class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class ShipmentListView(generics.ListCreateAPIView):
    queryset = Shipment.objects.select_related('order').all()
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]

class ShipmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shipment.objects.select_related('order').all()
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Optionally create a Customer record for the new user
            Customer.objects.create(
                user=user,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email
            )
            return Response(UserProfileSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def openapi_spec(request):
    # Adjust the path if you move the file
    spec_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'backend/openapi.yaml')
    return FileResponse(open(spec_path, 'rb'), content_type='application/yaml')
