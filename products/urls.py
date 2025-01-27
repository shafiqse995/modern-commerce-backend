""" Imports """

from typing import List
from django.urls import path  # type: ignore
from . import views

urlpatterns: List[path] = [
    path("", views.product_list_view, name="product-list"),
    path(r"category", views.product_category_list_view, name="product-category-list"),
]
