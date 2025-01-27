""" Imports """

from rest_framework.generics import ListAPIView, RetrieveAPIView  # type: ignore
from rest_framework.pagination import PageNumberPagination  # type: ignore
from rest_framework.filters import SearchFilter  # type: ignore
from .models import Product, ProductCategory
from .serializers import ProductCategorySerializer, ProductSerializer
from django_filters import rest_framework as filters  # type: ignore


class ProductListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ProductListFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = filters.BaseInFilter(field_name="category__id", lookup_expr="in")

    class Meta:
        model = Product
        fields = ["min_price", "max_price", "category"]


class ProductListAPIView(ListAPIView):
    """Product List API View"""

    queryset = Product.objects.all().order_by("-created_at")
    pagination_class = ProductListPagination
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, filters.DjangoFilterBackend]
    search_fields = ["title", "description", "category__title"]
    filterset_class = ProductListFilter


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
