from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from ..models.post_model import Post


def post_list_selector(request, view) -> QuerySet:
    """
    Fetches all active posts ordered by most recent.
    This logic is now centralized, so if we decide to change what
    defines an 'active' post, we only change it here.
    """
    queryset = Post.objects.filter(is_active=True).order_by('-created_at')

    for backend in view.filter_backends:
        queryset = backend().filter_queryset(request, queryset, view)

    return queryset


def post_detail_selector(post_id, user=None) -> Post:
    """
    Retrieves a specific post.
    If the user is not the owner, it only returns the post if it's active.
    """
    post = get_object_or_404(Post, pk=post_id)

    if not post.is_active and post.user != user:
        from django.http import Http404
        raise Http404("Post Not Available")

    return post
