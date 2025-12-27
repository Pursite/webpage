from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.lib.basemodel import BaseModel
from apps.post.models.post_model import Post


class Comment(BaseModel):
    """
        Represents a user's comment or reply on a specific post.

        This model supports a simple parent-child relationship for nested replies.

        Attributes:
            user (ForeignKey): The user who authored the comment.
            post (ForeignKey): The post being discussed.
            text (TextField): Content of the comment.
            parent (ForeignKey): Self-referential key to allow a single level of nesting (replies).
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f"{self.user.username} on Post {self.post_id}"