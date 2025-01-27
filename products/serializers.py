""" Imports """

from rest_framework import serializers  # type: ignore
from products.models import Product, ProductCategory


class ProductCategorySerializer(serializers.ModelSerializer):
    """Product Category Serializer"""

    class Meta:
        """Meta"""

        model = ProductCategory
        fields = ["id", "title"]


class ProductSerializer(serializers.ModelSerializer):
    """Product Serializer"""

    category = ProductCategorySerializer(read_only=True)

    class Meta:
        """Meta"""

        model = Product
        fields = ["id", "title", "description", "price", "category"]
