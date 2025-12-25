from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.product_model import Product
from ..serializers.product_list_serializer import ProductListSerializer
from ...lib.pagination import StandardPagePagination
from rest_framework import filters


class ProductListAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductListSerializer
    throttle_classes = [UserRateThrottle]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'brand']
    search_fields = ['name']

    def get(self, request):
        products = Product.objects.all().order_by('-created_at')

        for backend in list(self.filter_backends):
            products = backend().filter_queryset(request, products, self)

        paginator = StandardPagePagination()
        try:
            page = paginator.paginate_queryset(products, request, view=self)
            if page is not None:
                serializer = ProductListSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)