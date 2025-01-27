""" Imports """

from django.contrib import admin  # type: ignore
from .models import ProductCategory, Product

# Register your models here.
admin.site.register(ProductCategory)
admin.site.register(Product)
