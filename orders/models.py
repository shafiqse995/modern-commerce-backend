from django.db import models  # type: ignore
from django.utils.translation import gettext_lazy as _  # type: ignore
from django.core.validators import MinValueValidator  # type: ignore

from products.models import Product  # type: ignore


class OrderStatus(models.TextChoices):
    PENDING = ("pending", _("Pending"))
    CONFIRMED = ("confirmed", _("Confirmed"))
    DELIVERED = ("delivered", _("Delivered"))
    CANCELLED = ("cancelled", _("Cancelled"))


# Create your models here.
class Order(models.Model):
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )

    # customer information
    customer_id = models.CharField(max_length=255)
    customer_email = models.EmailField()

    # payment information
    payment_id = models.CharField(max_length=255)

    # Totals
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_order_status(self) -> OrderStatus:
        return OrderStatus(self.status)

    def __str__(self):
        return f"Order {self.order_id}"


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="line_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def save(self, *args, **kwargs):
        # If price isn't set, use current product price
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)
