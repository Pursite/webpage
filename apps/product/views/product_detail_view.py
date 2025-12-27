from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from ..models.product_model import Product
from ..serializers.product_detail_serializer import ProductDetailSerializer
from ..serializers.product_create_serializer import ProductCreateSerializer
from ...lib.permissions import IsAdminOrReadOnly
from ...lib.loggers import AppLogger


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
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductDetailSerializer(product)

        return Response(serializer.data)

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductCreateSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            AppLogger.log_activity(f"Product Updated (PUT) ID: {product.id}", user=request.user)
            return Response(serializer.data)

        AppLogger.log_activity(f"Product PUT Failed ID: {product.id} Errors: {serializer.errors}", user=request.user,
                               status="ERROR")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductCreateSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            AppLogger.log_activity(f"Product Updated (PATCH) ID: {product.id}", user=request.user)
            return Response(serializer.data)

        AppLogger.log_activity(f"Product PATCH Failed ID: {product.id} Errors: {serializer.errors}", user=request.user,
                               status="ERROR")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        p_id, p_name = product.id, product.name
        product.delete()
        AppLogger.log_activity(f"Product Deleted: {p_name} (ID: {p_id})", user=request.user)

        return Response({"detail": "Product Deleted"}, status=status.HTTP_204_NO_CONTENT)
