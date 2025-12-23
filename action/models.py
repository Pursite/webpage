from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from lib.basemodel import BaseModel
from post.models import Post

class Comment(BaseModel):
    text = models.TextField(_('text'))
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f"{self.user} - {self.post}"

