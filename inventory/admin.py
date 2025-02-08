from django.contrib import admin  # type:ignore
from .models import Inventory

admin.site.register(Inventory)
