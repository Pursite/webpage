from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from lib.basemodel import BaseModel
from product.models import Product

class Post(BaseModel):
    product = models.ForeignKey(Product, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=128, blank=True)
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    caption = models.TextField(_('caption'), blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return f"{self.user} Post ID: {self.id}"