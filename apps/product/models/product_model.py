from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.lib.basemodel import BaseModel
from apps.product.models.brand_model import Brand
from apps.product.models.category_model import Category


class Product(BaseModel):
    user = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE, blank=True)
    name = models.CharField(_("Product name"), max_length=255, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name="Category")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products', verbose_name="Brand")



    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return f"{self.name}"