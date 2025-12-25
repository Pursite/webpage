from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name="Category Title")
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title