from django.db import models

# Create your models here.
class Product(models.Model):
    stripe_product_id = models.CharField(default=None)
    user_id = models.IntegerField(default=None)
    name = models.CharField(max_length=100)
    price  = models.IntegerField(blank=False)
    description = models.TextField(blank=False)
    image = models.URLField()
    interval = models.CharField(default=None)
    created_at = models.DateTimeField(auto_now=True)