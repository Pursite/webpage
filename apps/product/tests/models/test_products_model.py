from django.test import TestCase, override_settings
from ..factories import ProductFactory, BrandFactory, CategoryFactory, UserFactory


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class ProductModelTest(TestCase):
    """
        Core test suite for the Product model.

        Ensures basic product creation, string representation,
        automatic timestamp generation (created_at), and validation
        of field constraints like maximum name length.
    """

    def setUp(self):
        self.brand = BrandFactory(name="Samsung")
        self.category = CategoryFactory(title="Mobile")
        self.user = UserFactory()

    def test_product_creation(self):
        product = ProductFactory(name="iPhone 15")
        self.assertEqual(str(product), "iPhone 15")
        self.assertTrue(product.created_at)

    def test_product_str_representation(self):
        product = ProductFactory(name="S23 Ultra")
        self.assertEqual(str(product), "S23 Ultra")

    def test_product_name_max_length(self):
        long_name = "A" * 256
        product = ProductFactory(name=long_name)
        with self.assertRaises(Exception):
            product.full_clean()
