from rest_framework import serializers
from .models import Product, Stock, Customer, ShoppingCart, ShoppingCartItem, Order, OrderItem, Shipment
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source='user', queryset=User.objects.all(), write_only=True, required=False)

    class Meta:
        model = Customer
        fields = ['id', 'user', 'user_id', 'first_name', 'last_name', 'email', 'address', 'created_at']

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

class ShipmentSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source='order.id', read_only=True)
    class Meta:
        model = Shipment
        fields = [
            'id', 'order', 'order_id', 'tracking_number', 'carrier', 'status', 'shipped_at', 'delivered_at', 'last_updated'
        ]

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
