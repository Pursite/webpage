from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.comment_model import PostComment
from ..serializers.comment_detail_serializer import CommentDetailSerializer
from ...lib.pagination import StandardPagePagination


class CommentListAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, post_id):
        comments = PostComment.objects.filter(post_id=post_id, parent=None).order_by('-created_at')

        paginator = StandardPagePagination()
        page = paginator.paginate_queryset(comments, request, view=self)

        if page is not None:
            serializer = CommentDetailSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = CommentDetailSerializer(comments, many=True)
        return Response(serializer.data)

