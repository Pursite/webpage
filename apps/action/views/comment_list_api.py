from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.comment_model import Comment
from ..serializers.comment_detail_serializer import CommentDetailSerializer
from ...lib.pagination import StandardPagePagination


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
        """
            Retrieves root comments (parent=None) for a given post_id.
            Implements pagination and orders by the most recent comments.
        """


        comments = Comment.objects.filter(
            post_id=post_id,
            parent=None
        ).select_related('user').prefetch_related('replies', 'replies__user').order_by('-created_at')

        paginator = StandardPagePagination()
        page = paginator.paginate_queryset(comments, request, view=self)

        if page is not None:
            serializer = CommentDetailSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = CommentDetailSerializer(comments, many=True)
        return Response(serializer.data)


