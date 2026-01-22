from ..models.post_model import Post


def post_list_selector() :
    """
    Fetches active posts based on filters.
    Converted to list for safe caching.
    """
    queryset = Post.objects.filter(is_active=True).select_related('user', 'product').order_by('-created_at')

    return queryset

