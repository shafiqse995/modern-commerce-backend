""" Imports """

from typing import List
from django.urls import path  # type: ignore
from . import views

urlpatterns: List[path] = [
    path("", views.product_list_view, name="product-list"),
    path(r"<int:id>", views.product_detail_view, name="product-detail"),
    path(r"category", views.product_category_list_view, name="product-category-list"),
    path(
        r"price-range",
        views.get_product_price_range,
        name="product-price-range",
    ),
]
