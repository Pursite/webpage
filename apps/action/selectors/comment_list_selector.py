from rest_framework.generics import get_object_or_404
from apps.post.models.post_model import Post
from ..models.comment_model import Comment
from ...lib.pagination import StandardPagePagination


def comment_list_selector(post_id: int, request, view) -> dict:
    """
    Fetches comments and handles pagination internally.
    Returns either a paginated response or a serialized list.
    """
    post = get_object_or_404(Post, pk=post_id, is_active=True)

    queryset = Comment.objects.filter(
        post=post,
        parent=None
    ).select_related('user').prefetch_related(
        'replies',
        'replies__user'
    ).order_by('-created_at')

    paginator = StandardPagePagination()
    page = paginator.paginate_queryset(queryset, request, view=view)

    return {
        "paginator": paginator,
        "page": page,
        "queryset": queryset
    }
