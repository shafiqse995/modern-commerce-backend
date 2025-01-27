""" Imports """

from django.apps import AppConfig  # type: ignore


class ProductsConfig(AppConfig):
    """Apps config for products app"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "products"
