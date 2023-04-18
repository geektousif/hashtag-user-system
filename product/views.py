# from django.shortcuts import render
from django.db.models.query import QuerySet
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
# from rest_framework.decorators import api_view, permission_classes
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
from .models import Product, MultipleImage
from .serializers import ProductSerializer, MultipleImageSerializer
from .scraper import flipkart_scraper
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
    lookup_url_kwarg = 'product_pk'

    def perform_create(self, serializer):
        pk = self.kwargs['product_pk']
        product = Product.objects.filter(id=pk).first()
        print(product)
        serializer.save(product=product)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(product__id=self.kwargs["product_pk"])


class ScrapeAndAddProduct(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        try:
            # req.body:- {"from": "flipkart", "product": "laptop", "no_items": 5}
            if (request.data["from"] == 'flipkart'):
                for product in flipkart_scraper(request.data["product"], request.data["no_items"]):
                    serializer = self.get_serializer(data=product)
                    # FIXME Object of type ValidationError is not JSON serializable
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
            return Response({"message": "Product fetched successfully"}, HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": e}, HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
