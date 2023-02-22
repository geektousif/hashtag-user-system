# from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView

from rest_framework.permissions import IsAdminUser, IsAuthenticated
# from rest_framework.decorators import api_view, permission_classes
from rest_framework import filters

from .models import Product, MultipleImage
from .serializers import ProductSerializer, MultipleImageSerializer

# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


# class ProductListView(ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [IsAuthenticated]


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class ProductSearchList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class MultipleImageViewSet(ModelViewSet):
    queryset = MultipleImage.objects.all()
    serializer_class = MultipleImageSerializer
    permission_classes = [IsAdminUser]
    lookup_url_kwarg = 'pk'

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        product = Product.objects.filter(id=pk).first()
        print(product)
        serializer.save(product=product)
