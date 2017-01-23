from rest_framework import viewsets
from . import serializers
from . import models


# Create your views here.

# CRUD views

# For Product
class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


# For Retailer
class RetailerViewSet(viewsets.ModelViewSet):
    queryset = models.Retailer.objects.all()
    serializer_class = serializers.RetailerSerializer
