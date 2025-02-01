""" Imports """

from rest_framework import serializers  # type: ignore
from products.models import Product, ProductCategory


class ProductCategorySerializer(serializers.ModelSerializer):
    """Product Category Serializer"""

    class Meta:
        """Product Category Serializer Meta"""

        model = ProductCategory
        fields = ["id", "title"]


class ProductSerializer(serializers.ModelSerializer):
    """Product Serializer"""

    category = ProductCategorySerializer(read_only=True)

    class Meta:
        """Product Serializer Meta"""

        model = Product
        fields = "__all__"
