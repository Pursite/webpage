from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from lib.basemodel import BaseModel


class Product(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)


    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return f"{self.user} Post ID: {self.id}"
