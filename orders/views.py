from decimal import Decimal
from django.conf import settings  # type: ignore
from django.http import HttpRequest, JsonResponse  # type: ignore
from rest_framework.decorators import api_view  # type: ignore
from django.db import transaction  # type: ignore
import stripe.error  # type: ignore
from orders.serializers import CustomerSerializer, PaymentIntentSerializer  # type: ignore
import stripe
from rest_framework import status  # type: ignore

from orders.services import OrderService  # type: ignore

stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(["POST"])
@transaction.atomic
def create_payment_intent(request: HttpRequest) -> JsonResponse:
    serializer = PaymentIntentSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)

    try:
        order_amount = sum(
            Decimal(str(item["price"])) * item["quantity"]
            for item in serializer.validated_data["line_items"]
        )
        amount_cents = int(order_amount * 100)  # Convert to cents for Stripe

        # Create payment intent
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency="eur",
            customer=serializer.validated_data.get("customer_id"),
            metadata={"line_items": str(serializer.validated_data["line_items"])},
        )

        customer = stripe.Customer.retrieve(serializer.validated_data["customer_id"])

        # create order
        order = OrderService.create_order(
            customer_id=serializer.validated_data["customer_id"],
            payment_intent_id=intent.id,
            customer_email=customer.email,
            line_items=serializer.validated_data["line_items"],
        )

        return JsonResponse(
            {
                "client_secret": intent.client_secret,
                "customer_id": serializer.validated_data.get("customer_id"),
                "order_id": order.id,
            },
            status=status.HTTP_201_CREATED,
        )
    except stripe.StripeError as e:
        return JsonResponse(
            {
                "error": str(e),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
def create_customer(request: HttpRequest) -> JsonResponse:
    serializer = CustomerSerializer(data=request.data)

    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)

    try:
        customer = stripe.Customer.create(
            email=serializer.validated_data["email"],
            name=serializer.validated_data["name"],
            phone=serializer.validated_data["phone"],
        )
        return JsonResponse(
            {
                "id": customer.id,
                "email": customer.email,
                "name": customer.name,
                "phone": customer.phone,
            },
            status=status.HTTP_201_CREATED,
        )

    except stripe.StripeError as e:
        return JsonResponse(
            {
                "error": str(e),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
