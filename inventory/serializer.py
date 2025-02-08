from rest_framework import serializers  # type: ignore
from inventory.models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    """Inventory Serializer"""

    quantity = serializers.IntegerField(default=0)

    class Meta:
        """Inventory Serializer Meta"""

        model = Inventory
        fields = ["quantity", "tracking"]
