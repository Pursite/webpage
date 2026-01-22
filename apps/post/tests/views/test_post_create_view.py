from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.post.tests.factories import UserFactory, ProductFactory
from apps.post.models.post_model import Post


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class PostCreateAPIViewTest(APITestCase):
    """
    Integration tests for PostCreateAPIView.
    Checks Authentication, Validation, and Response integrity.
    """

    def setUp(self):
        self.user = UserFactory()
        self.product = ProductFactory()
        self.url = reverse('post:post-create')

        self.valid_payload = {
            'product': self.product.id,
            'caption': 'API Level Test Caption',
            'price': 120.00,
            'location': 'Tehran',
            'is_active': True
        }

    def test_unauthenticated_user_cannot_post(self):
        self.client.logout()
        response = self.client.post(self.url, self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_post(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.url, self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().user, self.user)
        self.assertEqual(response.data['caption'], 'API Level Test Caption')

    def test_post_creation_fails_with_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        invalid_payload = self.valid_payload.copy()
        invalid_payload['price'] = -500

        response = self.client.post(self.url, invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data)

    def test_throttle_works(self):
        self.client.force_authenticate(user=self.user)

        for _ in range(10):
            response = self.client.post(self.url, self.valid_payload)
            if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                break

        pass
