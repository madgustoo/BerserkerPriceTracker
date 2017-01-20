from rest_framework import serializers
from . import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'image',
            'publication_date'
        )
        model = models.Product


class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'retailer_name',
            'price',
            'availability',
            'availability_note',
            'store_link',
            'updated_at'
        )
        model = models.Retailer
