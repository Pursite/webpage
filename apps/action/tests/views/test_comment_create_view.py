from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.action.models.comment_model import Comment
from apps.action.tests.factories import CommentFactory
from apps.post.tests.factories import PostFactory, UserFactory


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class CommentCreateAPIViewTest(APITestCase):
    """
    Tests for creating comments/replies via API.
    Verifies authentication, payload processing, and output format.
    """

    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory(is_active=True)
        self.url = reverse('action:comment-create')

        self.valid_payload = {
            'post': self.post.id,
            'text': 'Great post! Thanks for sharing.'
        }

    def test_unauthenticated_cannot_comment(self):
        self.client.logout()
        response = self.client.post(self.url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_comment(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.user.username)
        self.assertEqual(Comment.objects.count(), 1)

    def test_create_reply_via_api(self):
        parent_comment = CommentFactory(post=self.post)
        payload = {
            'post': self.post.id,
            'text': 'This is a reply to a comment.',
            'parent': parent_comment.id
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['parent'], parent_comment.id)

    def test_bad_request_on_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        invalid_payload = {'post': self.post.id, 'text': ''}

        response = self.client.post(self.url, invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
