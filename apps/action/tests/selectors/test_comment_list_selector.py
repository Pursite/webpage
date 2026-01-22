from django.test import TestCase, override_settings
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from rest_framework.views import APIView
from apps.action.selectors.comment_list_selector import comment_list_selector
from apps.action.tests.factories import CommentFactory
from apps.post.tests.factories import PostFactory


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class CommentListSelectorTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.post = PostFactory(is_active=True)
        self.other_post = PostFactory(is_active=True)

        self.parent_comment = CommentFactory(post=self.post, parent=None)
        self.reply = CommentFactory(post=self.post, parent=self.parent_comment)
        CommentFactory(post=self.other_post)

    def get_drf_request(self, url):
        django_request = self.factory.get(url)
        return Request(django_request)

    def test_selector_returns_only_top_level_comments(self):
        request = self.get_drf_request('/')
        result = comment_list_selector(post_id=self.post.id, request=request, view=APIView())

        self.assertEqual(result['queryset'].count(), 1)
        self.assertEqual(result['queryset'][0], self.parent_comment)

    def test_selector_prefetches_replies(self):
        request = self.get_drf_request('/')
        result = comment_list_selector(post_id=self.post.id, request=request, view=APIView())

        fetched_comment = result['queryset'][0]
        self.assertIn(self.reply, fetched_comment.replies.all())

    def test_selector_with_inactive_post_fails(self):
        self.post.is_active = False
        self.post.save()

        request = self.get_drf_request('/')
        with self.assertRaises(Exception):
            comment_list_selector(post_id=self.post.id, request=request, view=APIView())

    def test_pagination_logic(self):
        CommentFactory.create_batch(15, post=self.post, parent=None)

        request = self.get_drf_request('/?page=1')
        result = comment_list_selector(post_id=self.post.id, request=request, view=APIView())

        self.assertIsNotNone(result['page'])
