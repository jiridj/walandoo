import json
import random
from django.core.management.base import BaseCommand
from api.models import Product, Stock

class Command(BaseCommand):
    help = 'Load products from products.json and generate random stock for each product.'

    def handle(self, *args, **kwargs):
        with open('data/products.json', 'r') as f:
            products = json.load(f)
            for item in products:
                product, _ = Product.objects.update_or_create(
                    number=item['number'],
                    defaults={
                        'title': item['title'],
                        'price': item['price'],
                        'description': item['description'],
                        'category': item['category'],
                        'image': item['image'],
                        'rating_rate': item['rating']['rate'],
                        'rating_count': item['rating']['count'],
                    }
                )
                # Generate or update stock with a random quantity between 0 and 100
                Stock.objects.update_or_create(
                    product=product,
                    defaults={
                        'quantity': random.randint(0, 100)
                    }
                )
        self.stdout.write(self.style.SUCCESS('Products and stock loaded successfully.'))