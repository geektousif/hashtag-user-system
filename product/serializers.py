from rest_framework import serializers

from .models import Product, MultipleImage


class ProductSerializer(serializers.ModelSerializer):
    display_image = serializers.ImageField(
        max_length=None, allow_empty_file=False, allow_null=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'


class MultipleImageSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    image = serializers.ImageField(
        max_length=None, allow_empty_file=False, allow_null=True, required=False)

    class Meta:
        model = MultipleImage
        fields = '__all__'
