from typing import List
from django.urls import path  # type: ignore

from .views import create_payment_intent, create_customer

urlpatterns: List[path] = [
    path(r"payment/", create_payment_intent, name="create-payment-intent"),
    path(r"customer/", create_customer, name="create-customer"),
]
