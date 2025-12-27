from django.db import models


class Brand(models.Model):
    """
        Represents a product manufacturer or brand name.
        This model is used to categorize products by their brand (e.g., Apple, Nike).
    """

    name = models.CharField(max_length=100, unique=True, verbose_name="Brand Name")

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.name


class Category(models.Model):
    """
        Represents a product hierarchy or type.

        Includes a slug field for SEO-friendly URLs and support for Unicode characters.
    """

    title = models.CharField(max_length=100, unique=True, verbose_name="Category Title")
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title