from django.db import models  # type: ignore
from django.utils.translation import gettext_lazy as _  # type: ignore
from django.core.validators import MinValueValidator  # type: ignore
from django.core.mail import send_mail  # type: ignore
from modern_commerce.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string  # type: ignore
from django.utils.html import strip_tags  # type: ignore

from products.models import Product  # type: ignore


class OrderStatus(models.TextChoices):
    PENDING = ("pending", _("Pending"))
    COMPLETED = ("completed", _("Completed"))
    FAILED = ("failed", _("Failed"))


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

    def notify_customer(self):
        template = (
            "order-completed.html"
            if self.status == OrderStatus.COMPLETED
            else "order-failed.html"
        )
        subject = (
            "Order Placed" if self.status == OrderStatus.COMPLETED else "Order Failed"
        )
        context = {"order": self}
        html_message = render_to_string(template, context)
        plain_message = strip_tags(html_message)
        send_mail(
            subject=subject,
            html_message=html_message,
            message=plain_message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[self.customer_email],
        )

    def get_order_status(self) -> OrderStatus:
        return OrderStatus(self.status)

    def __str__(self):
        return f"""
            Order #{self.id} (
                status: {self.get_order_status()}
            )
        """


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
        return f"{self.product.title} ({self.quantity})"

    def save(self, *args, **kwargs):
        # If price isn't set, use current product price
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)
