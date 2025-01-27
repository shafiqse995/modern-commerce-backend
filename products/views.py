""" Imports """

from rest_framework.generics import ListAPIView, RetrieveAPIView  # type: ignore
from rest_framework.pagination import PageNumberPagination  # type: ignore

from .models import Product, ProductCategory
from .serializers import ProductCategorySerializer, ProductSerializer


class ProductListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ProductListAPIView(ListAPIView):
    """Product List API View"""

    pagination_class = ProductListPagination
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer


product_list_view = ProductListAPIView.as_view()


class ProductDetailAPIView(RetrieveAPIView):
    """Product Retrieve API View"""

    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    lookup_field = "id"


product_detail_view = ProductDetailAPIView.as_view()


class ProductCategoryListAPIView(ListAPIView):
    """Product Category List API View"""

    queryset = ProductCategory.objects.all().order_by("-created_at")
    serializer_class = ProductCategorySerializer


product_category_list_view = ProductCategoryListAPIView.as_view()
