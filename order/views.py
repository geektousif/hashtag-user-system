import json
from django.shortcuts import render
from django.db.models.query import QuerySet
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED
from rest_framework.mixins import UpdateModelMixin
from django.forms.models import model_to_dict

from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from product.models import Product
from product.serializers import ProductSerializer

# Create your views here.


class AddOrderItem(CreateAPIView, UpdateModelMixin):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'pk'

    def create(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        product_already = OrderItem.objects.filter(
            user=self.request.user, product__id=pk).first()

        if "quantity" not in self.request.data:
            self.request.data['quantity'] = 1

        if product_already:
            if product_already.product.units_available > 0:
                product_already.quantity += int(request.data['quantity'])
                data = model_to_dict(product_already)
                serializer = self.get_serializer(
                    product_already, data=data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({"message": "Product Not available"})
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        product = Product.objects.filter(id=pk).first()
        if product.units_available > 0:
            serializer.save(user=self.request.user,
                            product=product)


class RemoveOrderItem(DestroyAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = OrderItem.objects.filter(
            user=self.request.user, ordered=False)
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=HTTP_204_NO_CONTENT)


class ProductsInCart(ListAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = OrderItem.objects.filter(
            user=self.request.user, ordered=False)
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset


class PlaceOrder(CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        items = ProductsInCart.get_queryset(self)

        if len(items) <= 0:
            return Response({"message": "No item in cart"})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        for item in items:
            item.ordered = True
            item.save()
        serializer.save(user=user, order_items=items)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)
