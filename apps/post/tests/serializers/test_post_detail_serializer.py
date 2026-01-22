from django.test import TestCase, override_settings
from apps.post.serializers.post_detail_serializer import PostDetailSerializer
from apps.post.tests.factories import PostFactory, UserFactory
from apps.action.models.comment_model import Comment


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class PostDetailSerializerTest(TestCase):
    """
    Test suite for PostDetailSerializer.

    Verifies:
    - Correct nesting of Product information.
    - Logic for 'get_comments' (only root comments, max 10, descending order).
    - Accurate username mapping from the User model.
    """

    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.post = PostFactory(user=self.user, caption="Detail View Test")

        for i in range(12):
            Comment.objects.create(
                post=self.post,
                user=self.user,
                text=f"Root comment {i}",
                parent=None
            )

        root_comment = Comment.objects.first()
        Comment.objects.create(
            post=self.post,
            user=self.user,
            text="I am a reply",
            parent=root_comment
        )

    def test_serializer_contains_expected_fields(self):
        serializer = PostDetailSerializer(instance=self.post)
        data = serializer.data

        self.assertEqual(set(data.keys()), {"id", "product", "caption", "price", "user", "comments"})
        self.assertEqual(data['user'], "testuser")

    def test_get_comments_logic(self):
        serializer = PostDetailSerializer(instance=self.post)
        comments_data = serializer.data['comments']

        self.assertEqual(len(comments_data), 10)

        comment_texts = [c['text'] for c in comments_data]
        self.assertNotIn("I am a reply", comment_texts)

        latest_comment = Comment.objects.filter(parent__isnull=True).latest('created_at')
        self.assertEqual(comments_data[0]['text'], latest_comment.text)

    def test_product_data_is_nested(self):
        serializer = PostDetailSerializer(instance=self.post)
        product_data = serializer.data['product']

        self.assertIn('name', product_data)
        self.assertEqual(product_data['name'], self.post.product.name)
