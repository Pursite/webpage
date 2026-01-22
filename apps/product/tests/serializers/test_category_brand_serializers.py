from django.test import TestCase, override_settings
from apps.product.serializers.category_brand_serializer import CategorySerializer, BrandSerializer
from ..factories import CategoryFactory, BrandFactory


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class CategorySerializerTest(TestCase):
    """
        Test suite for Category serialization and validation.

        Ensures that category objects are correctly transformed into JSON and
        validates that required fields like 'title' and 'slug' are enforced
        during the deserialization process.
    """

    def test_category_serialization(self):
        category = CategoryFactory(title="Electronics", slug="electronics")
        serializer = CategorySerializer(category)

        expected_data = {
            'id': category.id,
            'title': "Electronics",
            'slug': "electronics"
        }
        self.assertEqual(serializer.data, expected_data)

    def test_category_deserialization_valid(self):
        data = {'title': 'Home Appliances', 'slug': 'home-appliances'}
        serializer = CategorySerializer(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['title'], 'Home Appliances')

    def test_category_missing_title(self):
        data = {'slug': 'home-appliances'}
        serializer = CategorySerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)


class BrandSerializerTest(TestCase):
    """
        Test suite for Brand serialization.

        Verifies the integrity of the output data for brands and confirms that
        the 'name' field is mandatory for valid API payloads.
    """

    def test_brand_serialization(self):
        brand = BrandFactory(name="Samsung")
        serializer = BrandSerializer(brand)

        expected_data = {
            'id': brand.id,
            'name': "Samsung"
        }
        self.assertEqual(serializer.data, expected_data)

    def test_brand_name_required(self):
        serializer = BrandSerializer(data={})

        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
