from django.test import TestCase, override_settings
from apps.post.serializers.post_list_serializer import PostListSerializer
from apps.post.tests.factories import PostFactory


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class PostListSerializerTest(TestCase):
    """
    Test suite for PostListSerializer.

    Verifies:
    - Proper mapping of nested product name to 'product_name' field.
    - All required lightweight fields are present in the output.
    - Read-only integrity of the serializer.
    """

    def setUp(self):
        self.post = PostFactory(
            caption="Amazing Product",
            price=250.00,
            location="Istanbul"
        )

    def test_serializer_returns_expected_fields(self):
        serializer = PostListSerializer(instance=self.post)
        expected_fields = {
            'id', 'product_name', 'caption', 'price',
            'location', 'created_at', 'is_active'
        }

        self.assertEqual(set(serializer.data.keys()), expected_fields)

    def test_product_name_mapping(self):
        serializer = PostListSerializer(instance=self.post)

        self.assertEqual(
            serializer.data['product_name'],
            self.post.product.name
        )

    def test_serializer_is_read_only_by_nature(self):
        serializer = PostListSerializer(instance=self.post)

        self.assertEqual(float(serializer.data['price']), 250.00)
        self.assertEqual(serializer.data['location'], "Istanbul")
