from rest_framework import serializers

from .models import Order, OrderItem
from product.serializers import ProductSerializer
from main.serializers import UserSerializer


class OrderItemSerializer(serializers.ModelSerializer):

    # user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = '__all__'
