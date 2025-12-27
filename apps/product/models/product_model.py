from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.lib.basemodel import BaseModel
from apps.product.models.category_brand_model import Category, Brand


class Product(BaseModel):
    """
        The master product catalog entity.

        This model serves as the reference for all user-generated posts.
        It contains core technical specifications like brand and category.

        Inherits from:
            BaseModel: Provides created_at and updated_at timestamps.
    """

    user = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE, blank=True)
    name = models.CharField(_("Product name"), max_length=255, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name="Category")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products', verbose_name="Brand")



    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return f"{self.name}"