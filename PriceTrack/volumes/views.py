from rest_framework.views import APIView
from rest_framework.views import Response
from . import serializers
from . import models


# Create your views here.

class ProductList(APIView):
    def get(self, request, format=None):
        products = models.Product.objects.all()
        serializer = serializers.ProductSerializer(products, many=True)
        return Response(serializer.data)


