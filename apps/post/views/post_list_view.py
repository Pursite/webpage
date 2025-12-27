from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from ..models.post_model import Post
from ..seializers.post_list_serializer import PostListSerializer
from ...lib.pagination import StandardPagePagination


class PostListAPIView(APIView):
    """
        Display a list of active advertisements.

        Features:
        - Filtering: Filter by 'product' ID or 'location'.
        - Searching: Search within 'caption' and 'location'.
        - Logic: Only displays posts where is_active=True.
        - Pagination: Implements StandardPagePagination.
    """


    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostListSerializer
    throttle_classes = [UserRateThrottle]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['product', 'location']
    search_fields = ['caption', 'location']

    def get(self, request):
        """
            List all active posts with applied filters and pagination.
        """


        posts = Post.objects.filter(is_active=True).order_by('-created_at')

        for backend in self.filter_backends:
            posts = backend().filter_queryset(request, posts, self)

        paginator = StandardPagePagination()
        page = paginator.paginate_queryset(posts, request, view=self)

        if page is not None:
            serializer = self.serializer_class(page, many=True)

            return paginator.get_paginated_response(serializer.data)

        serializer = self.serializer_class(posts, many=True)

        return Response(serializer.data)



