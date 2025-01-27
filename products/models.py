""" Imports """

from django.db import models  # type: ignore


class ProductCategory(models.Model):
    """Product Category Model"""

    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return str(self.title)


class Product(models.Model):
    """Product Model"""

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.title)
