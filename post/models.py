from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from lib.basemodel import BaseModel
from product.models import Product


class Post(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return f"{self.user} Post ID: {self.id}"
