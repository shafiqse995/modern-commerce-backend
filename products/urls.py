""" Imports """

from typing import List
from django.urls import path  # type: ignore
from . import views

urlpatterns: List[path] = [
    path("", views.product_list_create_view, name="product-list-create"),
    path(
        "<int:id>/", views.product_retrieve_update_destroy_view, name="product-detail"
    ),
]
