from django.db import IntegrityError, models
from django.test import TestCase, override_settings
from ..factories import ProductFactory, BrandFactory, CategoryFactory, UserFactory


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class ProductBrandAndCategoryModelTest(TestCase):
    """
        Test suite for Brand and Category models.

        Validates string representations, unique constraints (slugs),
        and deletion protection (on_delete=models.PROTECT) to ensure
        referential integrity between products and their taxonomy.
    """

    def setUp(self):
        self.brand = BrandFactory(name="Samsung")
        self.category = CategoryFactory(title="Mobile")
        self.user = UserFactory()

    def test_brand_str(self):
        brand = BrandFactory(name="Apple")
        self.assertEqual(str(brand), "Apple")

    def test_category_str(self):
        category = CategoryFactory(title="Electronics")
        self.assertEqual(str(category), "Electronics")

    def test_brand_deletion_protection(self):
        ProductFactory(brand=self.brand)
        with self.assertRaises(models.ProtectedError):
            self.brand.delete()

    def test_category_deletion_protection(self):
        ProductFactory(category=self.category)
        with self.assertRaises(models.ProtectedError):
            self.category.delete()

    def test_category_unique_slug_constraint(self):
        CategoryFactory(slug="test-slug")
        with self.assertRaises(IntegrityError):
            CategoryFactory(slug="test-slug")
