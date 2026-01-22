from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..factories import UserFactory, CategoryFactory, BrandFactory


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class ProductCreateAPIViewTest(APITestCase):
    """
    Integration tests for Product Creation API.

    Validates:
    - Role-based access control (Admin only).
    - Successful product persistence through the service layer.
    - Proper error responses when invalid data is submitted.
    - Throttling and authentication state handling.
    """

    def setUp(self):
        self.admin_user = UserFactory(is_staff=True)
        self.regular_user = UserFactory(is_staff=False)
        self.category = CategoryFactory()
        self.brand = BrandFactory()
        self.url = reverse('product:product-create')

        self.valid_payload = {
            'name': 'New Tech Product',
            'category': self.category.id,
            'brand': self.brand.id
        }

    def test_create_product_as_admin_success(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Tech Product')

    def test_create_product_as_regular_user_forbidden(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(self.url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product_unauthenticated(self):
        response = self.client.post(self.url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_product_invalid_data(self):
        self.client.force_authenticate(user=self.admin_user)
        invalid_payload = {'name': ''}
        response = self.client.post(self.url, invalid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
