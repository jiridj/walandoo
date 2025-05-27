from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'number', 'title', 'price', 'description',
            'category', 'image', 'rating_rate', 'rating_count'
        ]
