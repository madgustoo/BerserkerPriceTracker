from rest_framework import serializers
from . import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'image',
            'publication_date',
            'updated_at'
        )
        model = models.Product


class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'product',
            'retailer_name',
            'price',
            'availability',
            'availability_note',
            'store_link',
            'updated_at'
        )
        model = models.Retailer
