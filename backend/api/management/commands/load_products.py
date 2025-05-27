import json
from django.core.management.base import BaseCommand
from api.models import Product

class Command(BaseCommand):
    help = 'Load products from products.json'

    def handle(self, *args, **kwargs):
        with open('data/products.json', 'r') as f:
            products = json.load(f)
            for item in products:
                Product.objects.update_or_create(
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
        self.stdout.write(self.style.SUCCESS('Products loaded successfully.'))