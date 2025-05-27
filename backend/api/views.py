from django.shortcuts import render
from rest_framework import generics
from .models import Product, Stock, Customer, ShoppingCart, Order, Shipment
from .serializers import ProductSerializer, StockSerializer, CustomerSerializer, ShoppingCartSerializer, OrderSerializer, ShipmentSerializer

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

class CustomerListView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ShoppingCartListView(generics.ListCreateAPIView):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

class ShoppingCartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ShipmentListView(generics.ListCreateAPIView):
    queryset = Shipment.objects.select_related('order').all()
    serializer_class = ShipmentSerializer

class ShipmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shipment.objects.select_related('order').all()
    serializer_class = ShipmentSerializer
