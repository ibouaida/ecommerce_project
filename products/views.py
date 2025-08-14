from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Retourne seulement les produits en stock"""
        products = Product.objects.filter(stock__gt=0)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
