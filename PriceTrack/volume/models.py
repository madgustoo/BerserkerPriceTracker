from django.db import models


# Create your models here.

class Product(models.Model):
    product_id = models.PositiveIntegerField(primary_key=True)
    pub_date = models.DateTimeField('date published')
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=50)


class Retailer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    availability = models.CharField(max_length=100)

