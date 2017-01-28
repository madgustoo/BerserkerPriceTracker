from rest_framework import serializers
from . import models


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


class ProductSerializer(serializers.ModelSerializer):
    retailers = RetailerSerializer(many=True, read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'image',
            'publication_date',
            'updated_at',
            'retailers'
        )
        model = models.Product

