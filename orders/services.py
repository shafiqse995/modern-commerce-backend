from django.db import transaction  # type: ignore

from orders.models import Order, OrderLineItem, OrderStatus
from products.models import Product  # type: ignore


class OrderService:
    @staticmethod
    @transaction.atomic
    def create_order(
        customer_id: str,
        payment_intent_id: str,
        customer_email: str,
        line_items: list[OrderLineItem],
    ):
        product_ids = [item["product_id"] for item in line_items]
        products = Product.objects.filter(id__in=product_ids).in_bulk()

        # calculate order total
        total_amount = 0
        for item in line_items:
            amount = products.get(item["product_id"]).price * item["quantity"]
            total_amount += amount

        # create order
        order = Order.objects.create(
            customer_id=customer_id,
            customer_email=customer_email,
            payment_id=payment_intent_id,
            total_amount=total_amount,
            status="pending",
        )

        # create order items
        order_items = []
        for item in line_items:
            product = products[item["product_id"]]
            order_line_item = OrderLineItem(
                order=order,
                product=product,
                quantity=item["quantity"],
                price=product.price,
            )
            order_items.append(order_line_item)
        OrderLineItem.objects.bulk_create(order_items)

        return order

    @staticmethod
    def complete_order(payment_id: str):
        order = Order.objects.get(payment_id=payment_id)
        order_line_items = OrderLineItem.objects.all().filter(order=order)
        for line_item in order_line_items:
            line_item.product.update_inventory(line_item.quantity)
        order.status = OrderStatus.COMPLETED
        order.save()
        return order

    @staticmethod
    def fail_order(payment_id: str):
        order = Order.objects.get(payment_id=payment_id)
        order.status = OrderStatus.FAILED
        order.save()
        return order
