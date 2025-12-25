from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from apps.lib.permissions import IsAdminOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from ..models.product_model import Product
from ..serializers.product_detail_serializer import ProductDetailSerializer
from ..serializers.product_create_serializer import ProductCreateSerializer


class ProductDetailAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductDetailSerializer

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = self.serializer_class(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductCreateSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductCreateSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({"detail": "محصول حذف شد"}, status=status.HTTP_204_NO_CONTENT)
