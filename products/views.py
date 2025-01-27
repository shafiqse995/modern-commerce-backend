""" Imports """

from rest_framework.generics import ListAPIView  # type: ignore

from .models import Product, ProductCategory
from .serializers import ProductCategorySerializer, ProductSerializer


class ProductListAPIView(ListAPIView):
    """Product List API View"""

    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer


product_list_view = ProductListAPIView.as_view()


class ProductCategoryListAPIView(ListAPIView):
    """Product Category List API View"""

    queryset = ProductCategory.objects.all().order_by("-created_at")
    serializer_class = ProductCategorySerializer


product_category_list_view = ProductCategoryListAPIView.as_view()
