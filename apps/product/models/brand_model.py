from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Brand Name")

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name