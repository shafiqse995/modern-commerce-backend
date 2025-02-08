from typing import List
from django.urls import path  # type: ignore

from .views import create_payment_intent, handle_webhook

urlpatterns: List[path] = [
    path(r"payment/", create_payment_intent, name="create-payment-intent"),
    path(r"stripe/webhook", handle_webhook, name="stripe-webhook"),
]
