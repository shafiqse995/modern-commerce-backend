""" Imports """

from django.db import models  # type: ignore
from inventory.models import Inventory

from django.db.models.signals import post_save  # type:ignore
from django.dispatch import receiver  # type:ignore


class ProductCategory(models.Model):
    """Product Category Model"""

    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.title)


class Product(models.Model):
    """Product Model"""

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    media = models.ImageField(upload_to="uploads/")

    def check_inventory(self):
        pass

    def update_inventory(self):
        pass

    def __str__(self) -> str:
        return f"{self.title}"


@receiver(post_save, sender=Product)
def create_inventory_for_product(sender, instance, created, **kwargs):
    if created:
        Inventory.objects.create(product=instance, quantity=0)
