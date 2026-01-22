from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from ..serializers.product_create_serializer import ProductCreateSerializer
from ..services.product_create_service import product_create_service
from ...lib.permissions import IsAdmin


class ProductCreateAPIView(APIView):
    """
        Handle creation of new catalog products.

        Features:
        - Permission: Admin only (IsAdminOrReadOnly).
        - Throttling: Limits request frequency via UserRateThrottle.
        - Automation: Automatically assigns the logged-in user to the product.
    """

    permission_classes = [IsAdmin]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        product = product_create_service(user=request.user, data=request.data)
        serializer = ProductCreateSerializer(product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
