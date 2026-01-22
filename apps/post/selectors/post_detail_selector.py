from rest_framework.exceptions import NotFound
from ..models.post_model import Post


def post_detail_selector(post_id, user) -> Post:
    """
    Retrieves a single post with related product and user.
    """
    post = Post.objects.select_related('user', 'product').filter(pk=post_id).first()

    if not post:
        raise NotFound("Post Not Found")

    return post
