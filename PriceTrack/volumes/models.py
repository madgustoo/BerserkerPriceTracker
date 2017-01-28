from django.db import models
from django.utils import timezone


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    id = models.PositiveIntegerField(primary_key=True)
    publication_date = models.DateField('date published', null=True)
    image = models.CharField(max_length=100, null=True)
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        self.updated_at = timezone.now()
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Retailer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='retailers')
    retailer_name = models.CharField(max_length=100)
    price = models.FloatField(null=True)
    availability = models.BooleanField(default=False)
    availability_note = models.CharField(max_length=500, null=True)
    store_link = models.CharField(max_length=500, null=True)
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        self.updated_at = timezone.now()
        return super(Retailer, self).save(*args, **kwargs)

    class Meta:
        unique_together = ['retailer_name', 'product']

    def __str__(self):
        return self.retailer_name
