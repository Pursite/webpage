from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.post.tests.factories import UserFactory, PostFactory


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class PostDetailAPIViewTest(APITestCase):
    """
    Comprehensive tests for Post Detail API (GET, PUT, PATCH, DELETE).
    Focuses on Security, Ownership, and Data integrity.
    """

    def setUp(self):
        self.owner = UserFactory()
        self.stranger = UserFactory()
        self.post = PostFactory(user=self.owner, caption="Original Content", is_active=True)
        self.url = reverse('post:post-detail', kwargs={'pk': self.post.id})

    def test_get_post_detail_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.post.id)

    def test_owner_can_update_post(self):
        self.client.force_authenticate(user=self.owner)
        payload = {'caption': 'Updated Caption', 'product': self.post.product.id, 'price': 500}

        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.caption, 'Updated Caption')

    def test_stranger_cannot_update_post(self):
        self.client.force_authenticate(user=self.stranger)
        payload = {'caption': 'Hacked Content'}

        response = self.client.patch(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_owner_can_delete_post(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        if response.data:
            self.assertEqual(response.data['detail'], "Post Deleted")

        self.assertFalse(PostFactory._meta.model.objects.filter(id=self.post.id).exists())

    def test_stranger_cannot_delete_post(self):
        self.client.force_authenticate(user=self.stranger)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(PostFactory._meta.model.objects.filter(id=self.post.id).exists())

    def test_unauthenticated_cannot_modify(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
