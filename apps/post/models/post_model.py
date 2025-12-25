from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from apps.lib.basemodel import BaseModel
from apps.product.models.product_model import Product

class Post(BaseModel):
    product = models.ForeignKey(Product, related_name='posts', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    caption = models.TextField(_('caption'), blank=True)
    location = models.CharField(max_length=100, verbose_name=(_('location')), blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_('Price'))
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return f"{self.user.username} - {self.product.user}"

