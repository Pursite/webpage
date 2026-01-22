from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.throttling import UserRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from ..models.post_model import Post
from ..serializers.post_list_serializer import PostListSerializer
from ..selectors.post_list_selector import post_list_selector
from ...lib.pagination import StandardPagePagination
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


@method_decorator(cache_page(600), name='dispatch')
class PostListAPIView(APIView):
    """
        Display a list of active advertisements.

        Features:
        - Filtering: Filter by 'product' ID or 'location'.
        - Searching: Search within 'caption' and 'location'.
        - Logic: Only displays posts where is_active=True.
        - Pagination: Implements StandardPagePagination.
    """

    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['product', 'location']
    search_fields = ['caption', 'location']

    queryset = Post.objects.none()
    def get(self, request):
        """
            List all active posts with applied filters and pagination.
        """

        posts = post_list_selector()
        for backend in self.filter_backends:
            posts = backend().filter_queryset(request, posts, self)

        paginator = StandardPagePagination()
        page = paginator.paginate_queryset(posts, request, view=self)

        if page is not None:
            serializer = PostListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

