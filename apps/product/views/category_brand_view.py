from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from ..models.category_brand_model import Brand, Category
from ..serializers.category_brand_serializer import (
    CategorySerializer,
    BrandSerializer
)


class CategoryListAPIView(APIView):
    """
        Retrieve a list of all available product categories.

        Access: AllowAny (Public)
        Ordering: Sorted by ID.
        Used by: Frontend navigation and product filtering menus.
    """


    permission_classes = [AllowAny]

    def get(self, request):
        categories = Category.objects.all().order_by("id")
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data)


class BrandListAPIView(APIView):
    """
        Retrieve a list of all registered product brands.

        Access: AllowAny (Public)
        Ordering: Sorted by ID.
        Used by: Brand selection filters and product detail labels.
    """


    permission_classes = [AllowAny]

    def get(self, request):
        brands = Brand.objects.all().order_by("id")
        serializer = BrandSerializer(brands, many=True)

        return Response(serializer.data)