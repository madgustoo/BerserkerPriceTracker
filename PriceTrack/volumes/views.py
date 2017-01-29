from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.views.generic import TemplateView
from . import serializers
from . import models

""" View to App"""


class AppView(TemplateView):
    template_name = 'volumes/home.html'


""" API """


# For Product
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    """ /api/v1/product/1/retailers """

    @detail_route(methods=['get'])
    def retailers(self, request, pk=None):
        product = self.get_object()
        serializer = serializers.RetailerSerializer(
            product.retailers.all(), many=True
        )
        return Response(serializer.data)


# For Retailer
class RetailerViewSet(viewsets.ModelViewSet):
    queryset = models.Retailer.objects.all()
    serializer_class = serializers.RetailerSerializer
