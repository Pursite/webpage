from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.action.tests.factories import CommentFactory
from apps.post.tests.factories import PostFactory


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class CommentListAPIViewTest(APITestCase):
    """
    Tests for listing comments of a specific post.
    Verifies: Hierarchy, Post-isolation, and Pagination.
    """

    def setUp(self):
        self.post = PostFactory(is_active=True)
        self.other_post = PostFactory(is_active=True)
        self.url = reverse('action:post-comments-list', kwargs={'post_id': self.post.id})

        self.parent_comment = CommentFactory(post=self.post, text="Parent 1")
        self.reply = CommentFactory(post=self.post, parent=self.parent_comment, text="Reply 1")

        CommentFactory(post=self.other_post, text="Other Post Comment")

    def test_list_comments_success(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['text'], "Parent 1")

    def test_nested_replies_presence(self):
        response = self.client.get(self.url)

        parent_json = response.data['results'][0]
        self.assertEqual(len(parent_json['replies']), 1)
        self.assertEqual(parent_json['replies'][0]['text'], "Reply 1")

    def test_list_comments_pagination(self):
        CommentFactory.create_batch(15, post=self.post)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('next', response.data)

    def test_404_for_inactive_post(self):
        self.post.is_active = False
        self.post.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
