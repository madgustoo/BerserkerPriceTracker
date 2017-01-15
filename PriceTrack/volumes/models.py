from django.db import models


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=50)
    id = models.PositiveIntegerField(primary_key=True)
    publication_date = models.DateField('date published', null=True)
    image = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Retailer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    retailer_name = models.CharField(max_length=50)
    price = models.FloatField(default=0, null=True)
    availability = models.CharField(max_length=100, null=True)
    store_link = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.retailer_name
