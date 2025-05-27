from django.db import models

# Create your models here.

class Product(models.Model):
    number = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=100)
    image = models.CharField(max_length=255)
    rating_rate = models.FloatField()
    rating_count = models.IntegerField()

    def __str__(self):
        return self.title
