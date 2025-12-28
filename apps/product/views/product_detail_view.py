from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..selectors.selectors import product_detail_selector
from ..serializers.product_detail_serializer import ProductDetailSerializer
from ..serializers.product_create_serializer import ProductCreateSerializer
from apps.product.services.services import product_update_service, product_delete_service
from ...lib.permissions import IsAdminOrReadOnly


class ProductDetailAPIView(APIView):
    """
        Retrieve, update, or delete a specific product instance.

        Access:
        - GET: Public (IsAdminOrReadOnly).
        - PUT/PATCH/DELETE: Admin only (IsAdminOrReadOnly).

        Logging:
        - Logs every successful or failed update/delete action using AppLogger.
    """

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        product = product_detail_selector(product_id=pk)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = product_update_service(
            product_id=pk,
            user=request.user,
            data=request.data,
            partial=False
        )

        serializer = ProductCreateSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        product = product_update_service(product_id=pk, user=request.user, data=request.data, partial=True)
        serializer = ProductCreateSerializer(product)
        return Response(serializer.data)

    def delete(self, request, pk):
        product_delete_service(product_id=pk, user=request.user)
        return Response({"detail": "Product Deleted"}, status=status.HTTP_204_NO_CONTENT)
