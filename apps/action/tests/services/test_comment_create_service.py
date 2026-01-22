from django.test import TestCase, override_settings
from unittest.mock import patch
from rest_framework.exceptions import ValidationError
from apps.action.services.comment_create_service import comment_create_service
from apps.action.models.comment_model import Comment
from apps.action.tests.factories import CommentFactory
from apps.post.tests.factories import PostFactory, UserFactory


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class CommentCreateServiceTest(TestCase):
    """
    Tests the Comment Creation Service.
    Verifies database persistence and activity logging.
    """

    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory(is_active=True)
        self.valid_data = {
            'post': self.post.id,
            'text': 'This is a high-quality production comment.'
        }

    @patch('apps.lib.loggers.AppLogger.log_activity')
    def test_comment_create_success(self, mock_log):
        comment = comment_create_service(user=self.user, data=self.valid_data)

        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(comment.text, self.valid_data['text'])
        self.assertEqual(comment.user, self.user)

        mock_log.assert_called_once()
        self.assertIn("Comment created id=", mock_log.call_args[0][0])

    @patch('apps.lib.loggers.AppLogger.log_activity')
    def test_comment_create_validation_error_logging(self, mock_log):
        invalid_data = {'post': self.post.id, 'text': ''}

        with self.assertRaises(ValidationError):
            comment_create_service(user=self.user, data=invalid_data)

        self.assertEqual(mock_log.call_args[1]['status'], "ERROR")

    @patch('apps.lib.loggers.AppLogger.log_activity')
    def test_reply_creation_service(self, mock_log):
        parent = CommentFactory(post=self.post)
        reply_data = {
            'post': self.post.id,
            'text': 'Replying to the parent',
            'parent': parent.id
        }

        comment = comment_create_service(user=self.user, data=reply_data)

        self.assertEqual(comment.parent, parent)
        self.assertEqual(Comment.objects.count(), 2)
