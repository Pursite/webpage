from django.test import TestCase, override_settings
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory
from apps.action.serializers.comment_create_serializer import CommentCreateSerializer
from apps.action.tests.factories import CommentFactory
from apps.post.tests.factories import PostFactory, UserFactory


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class CommentCreateSerializerTest(TestCase):
    """
    Tests the validation logic of CommentCreateSerializer:
    - Max comments per user limit.
    - Parent-Post consistency.
    - Max nesting depth (1 level).
    """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()
        self.post = PostFactory()

        request = self.factory.get('/')
        request.user = self.user
        self.serializer_context = {'request': request}

    def test_validation_max_comments_limit(self):
        CommentFactory.create_batch(10, user=self.user, post=self.post)

        data = {
            'post': self.post.id,
            'text': 'This should fail'
        }
        serializer = CommentCreateSerializer(data=data, context=self.serializer_context)

        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        self.assertIn("10 users", str(cm.exception))

    def test_validation_parent_belongs_to_different_post(self):
        other_post = PostFactory()
        comment_on_other_post = CommentFactory(post=other_post)

        data = {
            'post': self.post.id,
            'text': 'Attempting cross-post reply',
            'parent': comment_on_other_post.id
        }
        serializer = CommentCreateSerializer(data=data, context=self.serializer_context)

        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        self.assertIn("someone else's post", str(cm.exception))

    def test_validation_max_depth_limit(self):
        parent = CommentFactory(post=self.post)
        reply = CommentFactory(post=self.post, parent=parent)  # لایه دوم

        data = {
            'post': self.post.id,
            'text': 'Attempting level 3 reply',
            'parent': reply.id
        }
        serializer = CommentCreateSerializer(data=data, context=self.serializer_context)

        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        self.assertIn("can't relpy anymore", str(cm.exception))

    def test_valid_comment_creation(self):
        data = {
            'post': self.post.id,
            'text': 'A valid comment'
        }
        serializer = CommentCreateSerializer(data=data, context=self.serializer_context)
        self.assertTrue(serializer.is_valid())
