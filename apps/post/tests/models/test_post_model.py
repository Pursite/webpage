from django.test import TestCase, override_settings
from django.db.utils import IntegrityError
from apps.post.tests.factories import PostFactory, UserFactory, ProductFactory
from apps.post.models.post_model import Post


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class PostModelTest(TestCase):
    """
    Comprehensive Test Suite for the Post Model.

    This class ensures that the Post model behaves correctly regarding its
    relationships, field constraints, default values, and metadata.
    """

    def setUp(self):
        """
        Set up initial data using factories for efficient testing.
        """
        self.post = PostFactory()

    def test_post_creation_with_factory(self):
        """
        Test if the Post instance is correctly created by the factory.

        Verifies that ForeignKeys (User and Product) are automatically
        instantiated and linked.
        """
        self.assertIsInstance(self.post, Post)
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())
        self.assertIsNotNone(self.post.user)
        self.assertIsNotNone(self.post.product)

    def test_post_string_representation(self):
        """
        Test the __str__ method of the Post model.

        Ensures the string output matches the format: {username} - {product_name}.
        """
        expected_str = f"{self.post.user.username} - {self.post.product.name}"
        self.assertEqual(str(self.post), expected_str)

    def test_post_default_values(self):
        """
        Test that default values are correctly applied when fields are omitted.
        """
        new_post = Post.objects.create(
            user=UserFactory(),
            product=ProductFactory()
        )
        self.assertEqual(new_post.price, 0.00)
        self.assertTrue(new_post.is_active)
        self.assertEqual(new_post.caption, "")
        self.assertEqual(new_post.location, "")

    def test_cascade_deletion_on_user(self):
        """
        Test that deleting a user also deletes their associated posts.
        """
        user = self.post.user
        user.delete()
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_cascade_deletion_on_product(self):
        """
        Test that deleting a product also deletes its associated posts.
        """
        product = self.post.product
        product.delete()
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_database_indexing(self):
        """
        Verify that the model Meta contains the expected indexes.

        Ensures performance optimizations for filtering by location and status are in place.
        """
        indexes = Post._meta.indexes
        indexed_fields = [index.fields for index in indexes]
        self.assertIn(['location', 'is_active'], indexed_fields)

    def test_integrity_error_on_missing_required_fields(self):
        """
        Test that Post cannot be created without required foreign keys.
        """
        with self.assertRaises(IntegrityError):
            Post.objects.create(user=None, product=None)
