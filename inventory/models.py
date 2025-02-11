from django.db import models  # type:ignore
from django.core.validators import MinValueValidator  # type: ignore
from django.utils.translation import gettext_lazy as _  # type: ignore
from django.core.mail import send_mail  # type: ignore
from modern_commerce.settings import EMAIL_HOST_USER, RECIPIENT_EMAIL
from django.template.loader import render_to_string  # type: ignore
from django.utils.html import strip_tags  # type: ignore

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
        if self.quantity <= 5:
            context = {
                "title": self.product.title,
                "quantity": self.quantity,
                "id": self.product.id,
            }
            html_message = render_to_string("low_stock_alert.html", context)
            plain_message = strip_tags(html_message)
            send_mail(
                subject=f"Low Stock Alert: {self.product.title}",
                html_message=html_message,
                message=plain_message,
                from_email=EMAIL_HOST_USER,
                recipient_list=[RECIPIENT_EMAIL],
            )
        self.save()

    def __str__(self):
        return f"{self.product} - {self.quantity} units"
