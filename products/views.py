""" Imports """

from django.http import JsonResponse, HttpRequest  # type: ignore
from rest_framework.generics import ListAPIView, RetrieveAPIView  # type: ignore
from rest_framework.pagination import PageNumberPagination  # type: ignore
from rest_framework.filters import SearchFilter  # type: ignore
from .models import Product, ProductCategory
from .serializers import ProductCategorySerializer, ProductSerializer
from django_filters import rest_framework as filters  # type: ignore
from rest_framework.decorators import api_view  # type: ignore
from rest_framework import status  # type: ignore
from django.db.models import Max, Min  # type: ignore


class ProductListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        response = {
            "count": self.page.paginator.count,
            "results": data,
            "next": self.page.next_page_number() if self.page.has_next() else None,
            "has_next": self.page.has_next(),
            "previous": (
                self.page.previous_page_number() if self.page.has_previous() else None
            ),
            "has_previous": self.page.has_previous(),
        }
        return JsonResponse(response)


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


@api_view(["GET"])
def get_product_price_range(request: HttpRequest) -> JsonResponse:
    """Product Min Max Price API View"""
    min_price = Product.objects.all().aggregate(Min("price")).get("price__min")
    max_price = Product.objects.all().aggregate(Max("price")).get("price__max")

    return JsonResponse(
        {
            "min_price": min_price if min_price is not None else "0",
            "max_price": max_price if max_price is not None else "1000",
        },
        status=status.HTTP_200_OK,
    )
