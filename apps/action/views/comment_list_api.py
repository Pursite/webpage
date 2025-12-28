from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from ..selectors.selectors import comment_list_selector
from ..serializers.comment_detail_serializer import CommentDetailSerializer


class CommentListAPIView(APIView):
    """
        View to list all top-level comments for a specific post.

        Access:
            Unauthenticated users can read comments (IsAuthenticatedOrReadOnly).

        Optimization:
            Uses select_related and prefetch_related to optimize database hits
            for users and nested replies.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, post_id):
        data = comment_list_selector(post_id=post_id, request=request, view=self)

        if data["page"] is not None:
            serializer = CommentDetailSerializer(data["page"], many=True)
            return data["paginator"].get_paginated_response(serializer.data)

        serializer = CommentDetailSerializer(data["queryset"], many=True)
        return Response(serializer.data)
