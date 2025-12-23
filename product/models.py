from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from lib.basemodel import BaseModel

class Product(BaseModel):
    user = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=64)


    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.title