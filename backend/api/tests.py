from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from .permissions import IsSelf
from .models import Product, Stock, Customer, ShoppingCart, ShoppingCartItem, Order, OrderItem, Shipment

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
        url = reverse('stock-detail', args=[self.product.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['quantity'], 7)
        self.assertEqual(response.data['product'], self.product.pk)

class CustomerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="john", email="john@example.com", password="testpass")
        self.customer = Customer.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            address="123 Main St"
        )

    def test_customer_str(self):
        self.assertEqual(str(self.customer), "John Doe")

    def test_customer_fields(self):
        self.assertEqual(self.customer.email, "john@example.com")
        self.assertEqual(self.customer.address, "123 Main St")

class CustomerAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testcustomer", email="testcustomer@example.com", password="testpass")
        self.customer = Customer.objects.create(
            user=self.user,
            first_name="Test",
            last_name="Customer",
            email="testcustomer@example.com"
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_retrieve_customer(self):
        url = reverse('customer-detail', args=[self.customer.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], "testcustomer@example.com")

class ShoppingCartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="jane", email="jane@example.com", password="testpass")
        self.customer = Customer.objects.create(
            user=self.user,
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com"
        )
        self.product = Product.objects.create(
            number=5,
            title="Cart Product",
            price=10.00,
            description="Cart test product.",
            category="cart-category",
            image="cart.jpg",
            rating_rate=4.2,
            rating_count=12
        )
        self.cart = ShoppingCart.objects.create(customer=self.customer)
        self.item = ShoppingCartItem.objects.create(cart=self.cart, product=self.product, quantity=3)

    def test_cart_str(self):
        self.assertIn(str(self.customer), str(self.cart))

    def test_cart_item_str(self):
        self.assertIn("Cart Product", str(self.item))
        self.assertIn(str(self.cart.id), str(self.item))

    def test_cart_item_fields(self):
        self.assertEqual(self.item.quantity, 3)
        self.assertEqual(self.item.product, self.product)
        self.assertEqual(self.item.cart, self.cart)

class ShoppingCartAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="cartuser", email="cartuser@example.com", password="testpass")
        self.customer = Customer.objects.create(
            user=self.user,
            first_name="Cart",
            last_name="User",
            email="cartuser@example.com"
        )
        self.cart = ShoppingCart.objects.create(customer=self.customer)
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_list_carts(self):
        url = reverse('cart-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_retrieve_cart(self):
        url = reverse('cart-detail', args=[self.cart.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer'], self.customer.pk)

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", email="alice@example.com", password="testpass")
        self.customer = Customer.objects.create(
            user=self.user,
            first_name="Alice",
            last_name="Wonder",
            email="alice@example.com"
        )
        self.product = Product.objects.create(
            number=6,
            title="Order Product",
            price=20.00,
            description="Order test product.",
            category="order-category",
            image="order.jpg",
            rating_rate=4.8,
            rating_count=22
        )
        self.order = Order.objects.create(customer=self.customer, total=40.00, status="pending")
        self.item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2, price=20.00)

    def test_order_str(self):
        self.assertIn(str(self.customer), str(self.order))

    def test_order_item_str(self):
        self.assertIn("Order Product", str(self.item))
        self.assertIn(str(self.order.id), str(self.item))

    def test_order_item_fields(self):
        self.assertEqual(self.item.quantity, 2)
        self.assertEqual(self.item.product, self.product)
        self.assertEqual(self.item.order, self.order)
        self.assertEqual(self.item.price, 20.00)

class OrderAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="orderuser", email="orderuser@example.com", password="testpass")
        self.customer = Customer.objects.create(
            user=self.user,
            first_name="Order",
            last_name="User",
            email="orderuser@example.com"
        )
        self.order = Order.objects.create(customer=self.customer, total=100.00, status="pending")
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_list_orders(self):
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_retrieve_order(self):
        url = reverse('order-detail', args=[self.order.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer'], self.customer.pk)

class ShipmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="bob", email="bob@example.com", password="testpass")
        self.customer = Customer.objects.create(
            user=self.user,
            first_name="Bob",
            last_name="Shipper",
            email="bob@example.com"
        )
        self.product = Product.objects.create(
            number=7,
            title="Shipped Product",
            price=30.00,
            description="Shipped test product.",
            category="ship-category",
            image="ship.jpg",
            rating_rate=4.0,
            rating_count=5
        )
        self.order = Order.objects.create(customer=self.customer, total=30.00, status="shipped")
        self.shipment = Shipment.objects.create(
            order=self.order,
            tracking_number="TRACK123",
            carrier="UPS",
            status="in transit"
        )

    def test_shipment_str(self):
        self.assertIn("TRACK123", str(self.shipment))
        self.assertIn(str(self.order.id), str(self.shipment))

    def test_shipment_fields(self):
        self.assertEqual(self.shipment.carrier, "UPS")
        self.assertEqual(self.shipment.status, "in transit")
        self.assertEqual(self.shipment.order, self.order)

class ShipmentAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="shipuser", email="shipuser@example.com", password="testpass")
        self.customer = Customer.objects.create(
            user=self.user,
            first_name="Ship",
            last_name="User",
            email="shipuser@example.com"
        )
        self.order = Order.objects.create(customer=self.customer, total=50.00, status="shipped")
        self.shipment = Shipment.objects.create(
            order=self.order,
            tracking_number="SHIP123",
            carrier="FedEx",
            status="delivered"
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_list_shipments(self):
        url = reverse('shipment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_retrieve_shipment(self):
        url = reverse('shipment-detail', args=[self.shipment.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tracking_number'], "SHIP123")
        self.assertEqual(response.data['order'], self.order.pk)

class RegistrationAPITest(APITestCase):
    def test_register_user(self):
        url = reverse('user-register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'TestPass123!',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)

class UserProfileAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='profileuser',
            email='profile@example.com',
            password='TestPass123!',
            first_name='Profile',
            last_name='User'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_profile(self):
        url = reverse('user-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'profileuser')

    def test_update_profile(self):
        url = reverse('user-profile')
        response = self.client.put(url, {'first_name': 'Changed'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Changed')

class IsSelfPermissionTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        from .models import Customer
        self.customer1 = Customer.objects.create(user=self.user1, first_name='A', last_name='B', email='a@b.com')
        self.customer2 = Customer.objects.create(user=self.user2, first_name='C', last_name='D', email='c@d.com')
        self.permission = IsSelf()

    def test_permission_allows_self(self):
        class DummyRequest: user = self.user1
        self.assertTrue(self.permission.has_object_permission(DummyRequest(), None, self.customer1))

    def test_permission_denies_other(self):
        class DummyRequest: user = self.user1
        self.assertFalse(self.permission.has_object_permission(DummyRequest(), None, self.customer2))
