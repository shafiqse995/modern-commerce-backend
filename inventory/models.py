from django.db import models  # type:ignore
from django.core.validators import MinValueValidator  # type: ignore
from django.utils.translation import gettext_lazy as _  # type: ignore


class Inventory(models.Model):
    product = models.OneToOneField(
        "products.Product",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="inventory",
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    tracking = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    def update_quantity(self, new_quantity: int):
        self.quantity -= new_quantity
        self.save()

    def __str__(self):
        return f"{self.product} - {self.quantity} units"
