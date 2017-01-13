from django.db import models


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=50)
    id = models.PositiveIntegerField(primary_key=True)
    price = models.FloatField(default=0)
    publication_date = models.DateTimeField('date published')
    image = models.CharField(max_length=50)
    availability = models.CharField(max_length=100)
    store_link = models.CharField(max_length=100)


class Retailer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    availability = models.CharField(max_length=100)


