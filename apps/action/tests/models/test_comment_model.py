from django.test import TestCase, override_settings
from apps.action.tests.factories import CommentFactory
from apps.post.tests.factories import PostFactory, UserFactory


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class CommentModelTest(TestCase):
    """
    Tests the integrity of the Comment model, specifically the
    parent-child relationship for replies.
    """

    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory()

    def test_comment_creation(self):
        comment = CommentFactory(user=self.user, post=self.post, text="This is a top-level comment")
        self.assertEqual(comment.post.comments.count(), 1)
        self.assertIsNone(comment.parent)

    def test_reply_to_comment(self):
        parent_comment = CommentFactory(post=self.post)
        reply = CommentFactory(
            post=self.post,
            parent=parent_comment,
            text="This is a reply"
        )

        self.assertEqual(parent_comment.replies.count(), 1)
        self.assertEqual(parent_comment.replies.first(), reply)
        self.assertEqual(reply.parent, parent_comment)

    def test_cascade_delete_post(self):
        CommentFactory(post=self.post)
        self.post.delete()
        self.assertEqual(CommentFactory._meta.model.objects.count(), 0)

    def test_str_method(self):
        comment = CommentFactory(user=self.user, post=self.post)
        expected_str = f"{self.user.username} on Post {self.post.id}"
        self.assertEqual(str(comment), expected_str)
