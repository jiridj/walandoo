from django.urls import path
from .views import (
    ProductListView, ProductDetailView,
    StockListView, StockDetailView,
    CustomerListView, CustomerDetailView,
    ShoppingCartListView, ShoppingCartDetailView,
    OrderListView, OrderDetailView,
    ShipmentListView, ShipmentDetailView,
    openapi_spec
)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('stock/', StockListView.as_view(), name='stock-list'),
    path('stock/<int:pk>/', StockDetailView.as_view(), name='stock-detail'),
    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('carts/', ShoppingCartListView.as_view(), name='cart-list'),
    path('carts/<int:pk>/', ShoppingCartDetailView.as_view(), name='cart-detail'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('shipments/', ShipmentListView.as_view(), name='shipment-list'),
    path('shipments/<int:pk>/', ShipmentDetailView.as_view(), name='shipment-detail'),
    path('openapi.yaml', openapi_spec, name='openapi-spec'),
]