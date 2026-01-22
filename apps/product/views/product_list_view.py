from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from ..selectors.product_list_selector import product_list_selector
from ..serializers.product_list_serializer import ProductListSerializer
from ...lib.pagination import StandardPagePagination
from ...lib.permissions import IsAdminOrReadOnly
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(600), name='dispatch')
class ProductListAPIView(APIView):
    """
        Advanced Product Catalog List View.

        Features:
        - Permissions: IsAdminOrReadOnly (Only admins can modify, everyone can view).
        - Throttling: UserRateThrottle applied to prevent API abuse.
        - Filtering: Supports filtering by 'category' and 'brand' via Query Parameters.
        - Search: Supports partial text search on the 'name' field.
        - Pagination: Returns paginated results based on StandardPagePagination settings.
    """

    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [UserRateThrottle]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'brand']
    search_fields = ['name']

    def get(self, request):
        products = product_list_selector()

        for backend in self.filter_backends:
            products = backend().filter_queryset(request, products, self)

        paginator = StandardPagePagination()
        page = paginator.paginate_queryset(products, request, view=self)

        if page is not None:
            serializer = ProductListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

