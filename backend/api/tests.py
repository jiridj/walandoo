from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product, Stock

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            number=1,
            title="Test Product",
            price=19.99,
            description="A test product.",
            category="test-category",
            image="test.jpg",
            rating_rate=4.5,
            rating_count=10
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Product")

    def test_product_fields(self):
        self.assertEqual(self.product.number, 1)
        self.assertEqual(self.product.price, 19.99)
        self.assertEqual(self.product.rating_rate, 4.5)

class ProductAPITest(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            number=2,
            title="API Product",
            price=29.99,
            description="API test product.",
            category="api-category",
            image="api.jpg",
            rating_rate=3.8,
            rating_count=5
        )

    def test_list_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_retrieve_product(self):
        url = reverse('product-detail', args=[self.product.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "API Product")

class StockModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            number=3,
            title="Stocked Product",
            price=49.99,
            description="A product with stock.",
            category="stock-category",
            image="stock.jpg",
            rating_rate=4.0,
            rating_count=20
        )
        self.stock = Stock.objects.create(
            product=self.product,
            quantity=15
        )

    def test_stock_str(self):
        self.assertIn("Stocked Product", str(self.stock))
        self.assertIn("15", str(self.stock))

    def test_stock_fields(self):
        self.assertEqual(self.stock.product, self.product)
        self.assertEqual(self.stock.quantity, 15)

class StockAPITest(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            number=4,
            title="API Stock Product",
            price=59.99,
            description="API stock test product.",
            category="api-stock-category",
            image="apistock.jpg",
            rating_rate=3.5,
            rating_count=8
        )
        self.stock = Stock.objects.create(
            product=self.product,
            quantity=7
        )

    def test_list_stocks(self):
        url = reverse('stock-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) >= 1)

    def test_retrieve_stock(self):
        url = reverse('stock-detail', args=[self.stock.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['quantity'], 7)
        self.assertEqual(response.data['product'], self.product.pk)
