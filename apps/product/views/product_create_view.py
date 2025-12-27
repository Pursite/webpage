from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from ..serializers.product_create_serializer import ProductCreateSerializer
from ...lib.permissions import IsAdminOrReadOnly
from ...lib.loggers import AppLogger


class ProductCreateAPIView(APIView):
    """
        Handle creation of new catalog products.

        Features:
        - Permission: Admin only (IsAdminOrReadOnly).
        - Throttling: Limits request frequency via UserRateThrottle.
        - Automation: Automatically assigns the logged-in user to the product.
    """


    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductCreateSerializer
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            product = serializer.save(user=request.user)

            AppLogger.log_activity(f"Product Created: {product.name} (ID: {product.id})", user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        AppLogger.log_activity(f"Product Create Failed: {serializer.errors}", user=request.user, status="ERROR")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
