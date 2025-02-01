from rest_framework import serializers  # type: ignore

from orders.models import Order, OrderLineItem
from products.serializers import ProductSerializer  # type: ignore


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderLineItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderLineItem
        fields = "__all__"


class CustomerSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=20)


class CartItemSerializer(serializers.Serializer):
    product_id = serializers.CharField(max_length=255)
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)


class PaymentIntentSerializer(serializers.Serializer):
    customer_id = serializers.CharField(required=False)
    line_items = CartItemSerializer(many=True, min_length=1)
