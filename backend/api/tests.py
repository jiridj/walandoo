from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product

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
