""" Imports """

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView  # type: ignore
from rest_framework.exceptions import NotFound  # type: ignore

from .models import Product, ProductCategory
from .serializers import ProductSerializer


class ProductListCreateAPIView(ListCreateAPIView):
    """Product List Create API View"""

    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer

    def perform_create(self, serializer: ProductSerializer) -> None:
        """Perform Create"""
        category_id = self.request.data.get("category")
        category = ProductCategory.objects.get(id=category_id)
        if category is None:
            raise NotFound(f"category with id {category_id} does not exist")

        serializer.save(**serializer.validated_data, category=category)


product_list_create_view = ProductListCreateAPIView.as_view()


class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """Product Detail API View"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"


product_retrieve_update_destroy_view = ProductRetrieveUpdateDestroyAPIView.as_view()
