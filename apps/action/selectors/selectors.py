from ..models.comment_model import Comment
from ...lib.pagination import StandardPagePagination


def comment_list_selector(post_id: int, request, view) -> dict:
    """
    Fetches comments and handles pagination internally.
    Returns either a paginated response or a serialized list.
    """
    queryset = Comment.objects.filter(
        post_id=post_id,
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
