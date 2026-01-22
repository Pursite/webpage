from django.test import TestCase, override_settings
from apps.action.serializers.comment_detail_serializer import CommentDetailSerializer
from apps.action.tests.factories import CommentFactory
from apps.post.tests.factories import PostFactory, UserFactory


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class CommentDetailSerializerTest(TestCase):
    """
    Tests the recursive display logic of CommentDetailSerializer.
    Verifies that:
    - Username is correctly mapped.
    - Top-level comments include their replies.
    - Replies themselves do not attempt to fetch further replies (Depth control).
    """

    def setUp(self):
        self.user = UserFactory(username="parsa_dev")
        self.post = PostFactory()

        self.parent_comment = CommentFactory(
            user=self.user,
            post=self.post,
            text="This is the parent",
            parent=None
        )

        self.reply = CommentFactory(
            user=self.user,
            post=self.post,
            text="This is a reply",
            parent=self.parent_comment
        )

    def test_serialized_fields_content(self):
        serializer = CommentDetailSerializer(instance=self.parent_comment)
        data = serializer.data

        self.assertEqual(data['user'], "parsa_dev")
        self.assertEqual(data['text'], "This is the parent")
        self.assertEqual(data['parent'], None)

    def test_recursive_replies_display(self):
        serializer = CommentDetailSerializer(instance=self.parent_comment)
        data = serializer.data

        self.assertTrue(len(data['replies']) > 0)
        self.assertEqual(data['replies'][0]['text'], "This is a reply")
        self.assertEqual(data['replies'][0]['parent'], self.parent_comment.id)

    def test_reply_depth_restriction(self):
        serializer = CommentDetailSerializer(instance=self.reply)
        data = serializer.data

        self.assertEqual(data['replies'], [])
