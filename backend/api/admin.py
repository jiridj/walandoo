from django.contrib import admin
from .models import Product, Stock, Customer, ShoppingCart, ShoppingCartItem, Order, OrderItem, Shipment

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'price', 'category', 'rating_rate', 'rating_count')
    search_fields = ('title', 'category')
    list_filter = ('category',)

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'last_updated')
    search_fields = ('product__title',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'created_at', 'checked_out')
    search_fields = ('customer__first_name', 'customer__last_name', 'customer__email')
    list_filter = ('checked_out',)

@admin.register(ShoppingCartItem)
class ShoppingCartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart__customer__email', 'product__title')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'created_at', 'total', 'status')
    search_fields = ('customer__first_name', 'customer__last_name', 'customer__email')
    list_filter = ('status',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__customer__email', 'product__title')

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('order', 'tracking_number', 'carrier', 'status', 'shipped_at', 'delivered_at', 'last_updated')
    search_fields = ('tracking_number', 'carrier', 'order__id')
    list_filter = ('status', 'carrier')
