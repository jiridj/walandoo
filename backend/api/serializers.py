from rest_framework import serializers
from .models import Product, Stock, Customer, ShoppingCart, ShoppingCartItem, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'number', 'title', 'price', 'description',
            'category', 'image', 'rating_rate', 'rating_count'
        ]

class StockSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product_title = serializers.CharField(source='product.title', read_only=True)

    class Meta:
        model = Stock
        fields = ['id', 'product', 'product_title', 'quantity', 'last_updated']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'address', 'created_at']

class ShoppingCartItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    class Meta:
        model = ShoppingCartItem
        fields = ['id', 'product', 'product_title', 'quantity']

class ShoppingCartSerializer(serializers.ModelSerializer):
    items = ShoppingCartItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.first_name', read_only=True)
    class Meta:
        model = ShoppingCart
        fields = ['id', 'customer', 'customer_name', 'created_at', 'checked_out', 'items']

class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_title', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.first_name', read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_name', 'created_at', 'total', 'status', 'items']
